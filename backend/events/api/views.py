from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from events.models import Event, TicketType
from .serializers import EventListSerializer,EventDetailSerializer, EventWriteSerializer,TicketTypeSerializer
from .permissions import IsOrganizer, IsOrganizerOwnerOrAdmin

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().select_related("organizer").prefetch_related("ticket_types")

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

    def perform_update(self, serializer):
        self.check_object_permissions(self.request, self.get_object())
        serializer.save()

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        instance.delete()

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsOrganizer])
    def publish(self, request, pk=None):
        event = self.get_object()
        if not (request.user.is_staff or event.organizer == request.user):
            return Response({"detail": "Нет доступа."}, status=status.HTTP_403_FORBIDDEN)

        event.status = Event.Status.PUBLISHED
        event.save(update_fields=["status"])
        return Response({"status": "Опубликовано."}, status=status.HTTP_200_OK)

class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all().select_related("event", "event__organizer")
    serializer_class = TicketTypeSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOwnerOrAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return qs
        return qs.filter(event__organizer=user)


    def perform_update(self, serializer):
        obj = self.get_object()
        if not (self.request.user.is_staff or obj.event.organizer == self.request.user):
            self.permission_denied(self.request, message="Нет доступа.")
        serializer.save()

    def perform_destroy(self, instance):
        if not (self.request.user.is_staff or instance.event.organizer == self.request.user):
            self.permission_denied(self.request, message="Нет доступа.")
        instance.delete()



