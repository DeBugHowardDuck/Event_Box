from decimal import Decimal
from django.conf import settings
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order, Ticket
from payments.models import Payment, WebhookEvent
from payments.services import (
    configure_yookassa,
    create_yookassa_payment,
    get_yookassa_payment,
)
from .serializers import YooKassaCreatePaymentSerializer
import hashlib
import json
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db import transaction
from payments.tasks import send_paid_order_email
from drf_spectacular.utils import extend_schema, OpenApiExample


class YooKassaCreatePaymentView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = YooKassaCreatePaymentSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        order_id = ser.validated_data["order_id"]

        order = Order.objects.select_related("user").get(id=order_id)

        if order.user != request.user and not request.user.is_staff:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        if order.status not in (Order.Status.NEW, Order.Status.PENDING_PAID):
            return Response(
                {"detail": f"Order status not payable: {order.status}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not settings.YOOKASSA_SHOP_ID or not settings.YOOKASSA_SECRET_KEY:
            return Response(
                {"detail": "YooKassa credentials are not configured"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        configure_yookassa(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)

        payment = create_yookassa_payment(
            amount_value=str(order.total_amount.quantize(Decimal("0.01"))),
            currency=order.currency,
            description=f"EventBox order #{order.id}",
            return_url=settings.YOOKASSA_RETURN_URL,
            order_id=order.id,
        )

        provider_payment_id = payment.id
        confirmation_url = payment.confirmation.confirmation_url

        order.status = Order.Status.PENDING_PAID
        order.provider = "yookassa"
        order.provider_payment_id = provider_payment_id
        order.provider_confirmation_url = confirmation_url
        order.save(
            update_fields=[
                "status",
                "provider",
                "provider_payment_id",
                "provider_confirmation_url",
            ]
        )

        Payment.objects.update_or_create(
            provider_payment_id=provider_payment_id,
            defaults={
                "order": order,
                "provider": Payment.Provider.YOOKASSA,
                "status": payment.status,
                "amount": order.total_amount,
                "currency": order.currency,
            },
        )

        return Response(
            {
                "order_id": order.id,
                "provider_payment_id": provider_payment_id,
                "status": payment.status,
                "confirmation_url": confirmation_url,
            },
            status=status.HTTP_201_CREATED,
        )


class YooKassaWebhookView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        body_bytes = request.body or b"{}"
        dedupe_key = hashlib.sha256(body_bytes).hexdigest()

        try:
            payload = json.loads(body_bytes.decode("utf-8"))
        except Exception:
            return Response({"detail": "invalid json"}, status=400)

        event_type = payload.get("event", "")
        obj = payload.get("object", {}) or {}
        payment_id = obj.get("id", "")

        wh, created = WebhookEvent.objects.get_or_create(
            dedupe_key=dedupe_key,
            defaults={
                "provider": "yookassa",
                "event_type": event_type,
                "object_id": payment_id,
                "raw_payload": payload,
            },
        )
        if not created:
            return Response(status=200)

        if payload.get("type") != "notification" or not event_type or not payment_id:
            return Response({"detail": "invalid notification"}, status=400)

        if not settings.YOOKASSA_SHOP_ID or not settings.YOOKASSA_SECRET_KEY:
            return Response({"detail": "yookassa credentials not configured"}, status=500)

        configure_yookassa(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)
        remote_payment = get_yookassa_payment(payment_id)

        remote_status = getattr(remote_payment, "status", "")
        remote_metadata = getattr(remote_payment, "metadata", {}) or {}
        order_id = remote_metadata.get("order_id")

        if not order_id:
            return Response({"detail": "missing order_id in payment metadata"}, status=400)

        wh.signature_ok = True
        wh.save(update_fields=["signature_ok"])

        with transaction.atomic():
            order = Order.objects.select_for_update().get(id=int(order_id))

            Payment.objects.update_or_create(
                provider_payment_id=payment_id,
                defaults={
                    "order": order,
                    "provider": Payment.Provider.YOOKASSA,
                    "status": remote_status,
                    "amount": order.total_amount,
                    "currency": order.currency,
                    "raw_payload": {
                        "id": payment_id,
                        "status": remote_status,
                        "metadata": remote_metadata,
                        "event": event_type,
                    },
                },
            )

            if event_type == "payment.succeeded":
                if order.status != Order.Status.PAID:
                    order.status = Order.Status.PAID
                    order.save(update_fields=["status"])

                    Ticket.objects.filter(order=order, status=Ticket.Status.PENDING).update(
                        status=Ticket.Status.ACTIVE
                    )
                    send_paid_order_email.delay(order.id)

            elif event_type == "payment.canceled":
                if order.status not in (Order.Status.PAID, Order.Status.REFUNDED):
                    order.status = Order.Status.CANCELED
                    order.save(update_fields=["status"])

        wh.processed_at = timezone.now()
        wh.save(update_fields=["processed_at"])

        return Response(status=200)
