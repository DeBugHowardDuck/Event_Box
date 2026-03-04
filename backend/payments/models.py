from django.db import models
from orders.models import Order
from django.utils import timezone


class Payment(models.Model):
    class Provider(models.TextChoices):
        YOOKASSA = "yookassa", "YooKassa"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    provider = models.CharField(
        max_length=32, choices=Provider.choices, default=Provider.YOOKASSA
    )

    status = models.CharField(max_length=32, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="RUB")

    provider_payment_id = models.CharField(max_length=128, unique=True)
    raw_payload = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.provider_payment_id} ({self.status})"


class WebhookEvent(models.Model):
    provider = models.CharField(max_length=32, default="yookassa")
    dedupe_key = models.CharField(max_length=32, unique=True)
    event_type = models.CharField(max_length=64)
    object_id = models.CharField(max_length=128, blank=True)

    signature_ok = models.BooleanField(default=False)
    processed_at = models.DateTimeField(blank=True, null=True)

    raw_payload = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_processed(self):
        self.processed_at = timezone.now()
        self.save(update_fields=["processed_at"])
