from django.contrib import admin
from .models import Order, Ticket


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "event", "status", "total_amount", "currency", "created_at")
    list_filter = ("status", "currency")
    search_fields = ("id", "user__email", "event__title")
    ordering = ("-created_at",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "ticket_type", "status", "code", "used_at")
    list_filter = ("status",)
    search_fields = ("code", "qr_payload", "order__id")
    ordering = ("-id",)