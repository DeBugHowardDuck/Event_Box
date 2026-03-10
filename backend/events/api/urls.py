from rest_framework.routers import DefaultRouter
from .views import EventViewSet, TicketTypeViewSet
from .views import OrganizerMyEventsView
from django.urls import path


router = DefaultRouter()
router.register(r"events", EventViewSet, basename="events")
router.register(r"ticket-types", TicketTypeViewSet, basename="ticket-types")

urlpatterns = [
    path("organizer/events/", OrganizerMyEventsView.as_view(), name="organizer-my-events" ),
]

urlpatterns += router.urls
