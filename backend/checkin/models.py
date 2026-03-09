from django.conf import settings
from django.db import models
from django.utils import timezone

from orders.models import Ticket

class CheckIn(models.Model):
    class Result(models.TextChoices):
        OK = "ok", "OK"
        INVALID = "invalid", "Invalid"
        ALREDY_USED = "alredy used", "Alredy Used"
        NOT_ACTIVE = "not active", "Not Active"

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="checkins")
    checker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="checkins")

    scanned_at = models.DateTimeField(default=timezone.now)
    result = models.CharField(max_length=20, choices=Result.choices)
    meta = models.JSONField(default=dict)

    def __str__(self):
        return f"CheckIn {self.ticket_id}{self.result}"