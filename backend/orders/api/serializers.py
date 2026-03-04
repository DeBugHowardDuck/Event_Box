from rest_framework import serializers
from django.utils import timezone

from events.models import Event, TicketType
from orders.models import Order, Ticket
from orders.services import make_ticket_payload


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "ticket_type",
            "code",
            "qr_payload",
            "status",
            "used_at",
            "created_at",
        )


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "event",
            "total_amount",
            "currency",
            "provider",
            "created_at",
            "tickets",
        )


class OrderCreateSerializer(serializers.Serializer):
    ticket_type_id = serializers.IntegerField()
    qty = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, attrs):
        ticket_type_id = attrs["ticket_type_id"]
        qty = attrs["qty"]

        try:
            tt = TicketType.objects.select_related("event").get(id=ticket_type_id)
        except TicketType.DoesNotExist:
            raise serializers.ValidationError("ticket_type_id не найден")

        event = tt.event
        now = timezone.now()

        if event.status != Event.Status.PUBLISHED:
            raise serializers.ValidationError("Мероприятие не опубликовано")

        if event.registration_ends_at and event.registration_ends_at <= now:
            raise serializers.ValidationError("Регистрация закрыта")

        if not tt.is_active:
            raise serializers.ValidationError("Тип билета не активен")

        if tt.sales_start and tt.sales_start > now:
            raise serializers.ValidationError("Продажи еще не начались")

        if tt.sales_end and tt.sales_end <= now:
            raise serializers.ValidationError("Продажи завершены")

        if tt.quota and qty > tt.quota:
            raise serializers.ValidationError("qty превышает quota этого типа билетов")

        attrs["ticket_type"] = tt
        attrs["event"] = event
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        tt = validated_data["ticket_type"]
        event = validated_data["event"]
        qty = validated_data["qty"]

        total = tt.price * qty

        order = Order.objects.create(
            user=user,
            event=event,
            status=Order.Status.NEW,
            total_amount=total,
            currency=tt.currency,
            provider="yookassa",
        )

        tickets = []
        for _ in range(qty):
            ticket = Ticket(order=order, ticket_type=tt)
            ticket.qr_payload = make_ticket_payload(ticket.code)
            tickets.append(ticket)

        Ticket.objects.bulk_create(tickets)
        return order
