from django.conf import settings
from django.db import models
from django.utils import timezone

class Event(models.Model):
    class VenueType(models.TextChoices):
        ONLINE = "online", "Online"
        OFFLINE = "offline", "Offline"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CANCELLED = "cancelled", "Cancelled"

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="event_covers/", null=True, blank=True)

    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    timezone = models.CharField(max_length=64, default="Europe/Moscow")

    venue_type = models.CharField(max_length=20, choices=VenueType.choices)
    venue_address = models.CharField(max_length=500, blank=True)
    online_url = models.URLField(blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    capacity = models.PositiveIntegerField(default=0)
    registration_ends_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.starts_at and self.ends_at and self.starts_at >= self.ends_at:
            raise ValueError("starts_at должен быть ends_at")

        if self.venue_type == self.VenueType.ONLINE and not self.online_url:
            raise ValueError("Для онлайн события нужен online_url")
        if self.venue_type == self.VenueType.OFFLINE and not self.venue_address:
            raise ValueError("Для офлайн события необходим venue_address")

        if self.registration_ends_at and self.starts_at and self.registration_ends_at > self.starts_at:
            raise ValueError("registration_ends_at не может быть позже starts_at")

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class TicketType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket_types")

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="RUB")

    quota = models.PositiveIntegerField(default=0)
    sales_start = models.DateTimeField(null=True, blank=True)
    sales_end = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.sales_start and self.sales_end and self.sales_start > self.sales_end:
            raise ValueError("sales_start должен быть меньше sales_end")

    def __str__(self):
        return f"{self.event.title} / {self.name}"