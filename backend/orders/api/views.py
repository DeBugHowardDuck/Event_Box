from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order, Ticket
from .serializers import OrderSerializer, OrderCreateSerializer, TicketSerializer

class OrderCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        self.order = serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        out = OrderSerializer(order).data
        return self.get_response(out)

    def get_response(self, data):
        return Response(data, status=status.HTTP_201_CREATED)

class MyOrdersView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("tickets").order_by("-created_at")


class MyTicketsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(order__user=self.request.user).select_related('ticket_type', 'order').order_by('-created_at')