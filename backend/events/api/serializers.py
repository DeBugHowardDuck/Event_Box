from django.utils import timezone
from rest_framework import serializers

from events.models import Event, TicketType


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = (
            "id",
            "event",
            "name",
            "price",
            "currency",
            "quota",
            "sales_start",
            "sales_end",
            "is_active",
        )
        read_only_fields = ("id",)


class TicketTypePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = (
            "id",
            "name",
            "price",
            "currency",
            "quota",
            "sales_start",
            "sales_end",
            "is_active",
        )


class EventListSerializer(serializers.ModelSerializer):
    tickets_left = serializers.SerializerMethodField()
    is_sold_out = serializers.SerializerMethodField()
    is_registration_closed = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "starts_at",
            "ends_at",
            "timezone",
            "venue_type",
            "status",
            "capacity",
            "registration_ends_at",
            "tickets_left",
            "is_sold_out",
            "is_registration_closed",
        )

    def get_tickets_left(self, obj: Event):
        total_quota = sum(tt.quota for tt in obj.ticket_types.filter(is_active=True))
        if obj.capacity and total_quota:
            return min(obj.capacity, total_quota)
        if obj.capacity:
            return obj.capacity
        return total_quota

    def get_is_sold_out(self, obj: Event):
        return self.get_tickets_left(obj) == 0

    def get_is_registration_closed(self, obj: Event):
        if obj.registration_ends_at is None:
            return False
        return obj.registration_ends_at <= timezone.now()


class EventDetailSerializer(serializers.ModelSerializer):
    ticket_types = TicketTypePublicSerializer(many=True, read_only=True)
    tickets_left = serializers.SerializerMethodField()
    is_sold_out = serializers.SerializerMethodField()
    is_registration_closed = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            "id",
            "organizer",
            "title",
            "description",
            "cover_image",
            "starts_at",
            "ends_at",
            "timezone",
            "venue_type",
            "venue_address",
            "online_url",
            "status",
            "capacity",
            "registration_ends_at",
            "ticket_types",
            "tickets_left",
            "is_sold_out",
            "is_registration_closed",
        )

    def get_tickets_left(self, obj: Event):
        total_quota = sum(tt.quota for tt in obj.ticket_types.filter(is_active=True))
        if obj.capacity and total_quota:
            return min(obj.capacity, total_quota)
        if obj.capacity:
            return obj.capacity
        return total_quota

    def get_is_sold_out(self, obj: Event):
        return self.get_tickets_left(obj) == 0

    def get_is_registration_closed(self, obj: Event):
        if obj.registration_ends_at is None:
            return False
        return obj.registration_ends_at <= timezone.now()


class EventWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "cover_image",
            "starts_at",
            "ends_at",
            "timezone",
            "venue_type",
            "venue_address",
            "online_url",
            "status",
            "capacity",
            "registration_ends_at",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        starts_at = attrs.get("starts_at", getattr(self.instance, "starts_at", None))
        ends_at = attrs.get("ends_at", getattr(self.instance, "ends_at", None))
        venue_type = attrs.get("venue_type", getattr(self.instance, "venue_type", None))
        venue_address = attrs.get("venue_address", getattr(self.instance, "venue_address", ""))
        online_url = attrs.get("online_url", getattr(self.instance, "online_url", ""))
        registration_ends_at = attrs.get("registration_ends_at", getattr(self.instance, "registration_ends_at", None))

        if starts_at and ends_at and starts_at >= ends_at:
            raise serializers.ValidationError("starts_at должен быть меньше ends_at")

        if venue_type == Event.VenueType.ONLINE and not online_url:
            raise serializers.ValidationError("Для online события нужен online_url")

        if venue_type == Event.VenueType.OFFLINE and not venue_address:
            raise serializers.ValidationError("Для offline события нужен venue_address")

        if registration_ends_at and starts_at and registration_ends_at > starts_at:
            raise serializers.ValidationError("registration_ends_at не может быть позже starts_at")

        return attrs
