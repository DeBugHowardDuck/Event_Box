from decimal import Decimal
from django.conf import settings
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order
from payments.models import Payment
from payments.services import configure_yookassa, create_yookassa_payment
from .serializers import YooKassaCreatePaymentSerializer


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
            return Response({"detail": f"Order status not payable: {order.status}"}, status=status.HTTP_400_BAD_REQUEST)

        if not settings.YOOKASSA_SHOP_ID or not settings.YOOKASSA_SECRET_KEY:
            return Response({"detail": "YooKassa credentials are not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        order.save(update_fields=["status", "provider", "provider_payment_id", "provider_confirmation_url"])

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