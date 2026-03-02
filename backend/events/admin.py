from django.contrib import admin
from .models import Event, TicketType

class TicketTypeInline(admin.TabularInline):
    model = TicketType
    extra = 0

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "organizer", "status", "starts_at", "venue_type", "capacity")
    list_filter = ("status", "venue_type")
    search_fields = ("title", "description")
    date_hierarchy = "starts_at"
    inlines = [TicketTypeInline]

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "name", "price", "currency", "quota", "is_active")
    list_filter = ("currency", "is_active")
    search_fields = ("name", 'event__title')