from rest_framework.routers import DefaultRouter
from .views import EventViewSet, TicketTypeViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="events")
router.register(r"ticket-types", TicketTypeViewSet, basename="ticket-types")

urlpatterns = router.urls