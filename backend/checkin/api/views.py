from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from orders.models import Ticket
from checkin.models import CheckIn
from .serializers import CheckInQRSerializer
from .permissions import IsCheckerOrAdmin


class CheckInQRView(APIView):
    permission_classes = [IsCheckerOrAdmin]

    def post(self, request):
        ser = CheckInQRSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        qr_payload = ser.validated_data["qr_payload"].strip()

        with transaction.atomic():
            ticket = Ticket.objects.select_for_update().select_related("order").filter(qr_payload=qr_payload).first()

            if not ticket:
                return Response({"result": "invalid"}, status=status.HTTP_200_OK)

            if ticket.status == Ticket.Status.USED:
                CheckIn.objects.create(ticket=ticket, checker=request.user, result=CheckIn.Result.ALREDY_USED)
                return Response({"result": "already_used"}, status=status.HTTP_200_OK)

            if ticket.status != Ticket.Status.ACTIVE:
                CheckIn.objects.create(ticket=ticket, checker=request.user, result=CheckIn.Result.NOT_ACTIVE)
                return Response({"result": "not_active"}, status=status.HTTP_200_OK)

            # OK: помечаем used
            ticket.status = Ticket.Status.USED
            ticket.used_at = timezone.now()
            ticket.save(update_fields=["status", "used_at"])

            CheckIn.objects.create(ticket=ticket, checker=request.user, result=CheckIn.Result.OK)

        return Response(
            {
                "result": "ok",
                "ticket_id": ticket.id,
                "order_id": ticket.order_id,
                "used_at": ticket.used_at,
            },
            status=status.HTTP_200_OK,
        )
