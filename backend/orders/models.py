import uuid
from django.conf import settings
from django.db import models
from events.models import Event, TicketType


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        PENDING_PAID = "pending_paid", "Pending_paid"
        PAID = "paid", "Paid"
        CANCELED = "canceled", "Canceled"
        EXPIRED = "expired", "Expired"
        REFUNDED = "refunded", "Refunded"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="orders")

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="RUB")

    provider = models.CharField(max_length=32, default="yookassa")
    provider_payment_id = models.CharField(max_length=120, blank=True)
    provider_confirmation_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Заказ#{self.id}{self.status}"


class Ticket(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACTIVE = "active", "Active"
        USED = "used", "Used"
        REFUNDED = "refunded", "Refunded"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")
    ticket_type = models.ForeignKey(
        TicketType, on_delete=models.PROTECT, related_name="tickets"
    )

    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    qr_payload = models.CharField(max_length=255, unique=True)

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    used_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Билет {self.code} ({self.status})"
