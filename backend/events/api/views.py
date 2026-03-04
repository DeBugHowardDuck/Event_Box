from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from events.models import Event, TicketType
from .serializers import (
    EventListSerializer,
    EventDetailSerializer,
    EventWriteSerializer,
    TicketTypeSerializer,
)
from .permissions import IsOrganizer, IsOrganizerOwnerOrAdmin
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EventFilter
from django.core.cache import cache
from common.cache_keys import events_list_key, events_detail_key, bump_events_version


class EventViewSet(viewsets.ModelViewSet):
    queryset = (
        Event.objects.all().select_related("organizer").prefetch_related("ticket_types")
    )

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filter_class = EventFilter

    search_fields = ["title", "description"]

    ordering_fields = ["starts_at", "ends_at", "created_at"]
    ordering = "starts_at"

    def list(self, request, *args, **kwargs):
        key = events_list_key(request.query_params)
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(key, response.data, timeout=60)
        return response

    def retrieve(self, request, *args, **kwargs):
        event_id = kwargs.get("pk")
        key = events_detail_key(int(event_id))
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(key, response.data, timeout=120)
        return response

    def get_serializer_class(self):
        if self.action == "list":
            return EventListSerializer
        if self.action == "retrieve":
            return EventDetailSerializer
        return EventWriteSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]

        return [IsAuthenticated(), IsOrganizer()]

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action in ("list", "retrieve"):
            return qs.filter(status=Event.Status.PUBLISHED)

        user = self.request.user
        if user.is_staff:
            return qs
        return qs.filter(organizer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)
        bump_events_version()

    def perform_update(self, serializer):
        self.check_object_permissions(self.request, self.get_object())
        serializer.save()
        bump_events_version()

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        instance.delete()
        bump_events_version()

    @action(
        detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsOrganizer]
    )
    def publish(self, request, pk=None):
        event = self.get_object()
        if not (request.user.is_staff or event.organizer == request.user):
            return Response(
                {"detail": "Нет доступа."}, status=status.HTTP_403_FORBIDDEN
            )

        event.status = Event.Status.PUBLISHED
        event.save(update_fields=["status"])
        bump_events_version()
        return Response({"status": "Опубликовано."}, status=status.HTTP_200_OK)


class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all().select_related("event", "event__organizer")
    serializer_class = TicketTypeSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOwnerOrAdmin]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["event", "is_active", "currency"]
    ordering_fields = ["price", "created_at"]
    ordering = ["price"]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return qs
        return qs.filter(event__organizer=user)

    def perform_create(self, serializer):
        obj = serializer.save()
        bump_events_version()
        return obj

    def perform_update(self, serializer):
        obj = self.get_object()
        if not (self.request.user.is_staff or obj.event.organizer == self.request.user):
            self.permission_denied(self.request, message="Нет доступа.")
        serializer.save()
        bump_events_version()
        return obj

    def perform_destroy(self, instance):
        if not (
                self.request.user.is_staff or instance.event.organizer == self.request.user
        ):
            self.permission_denied(self.request, message="Нет доступа.")
        instance.delete()
        bump_events_version()

