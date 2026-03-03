from django.urls import path
from .views import OrderCreateView, MyOrdersView, MyTicketsView

urlpatterns = [
    path('orders/', OrderCreateView.as_view(), name='order-create'),
    path('orders/my/', MyOrdersView.as_view(), name='my-orders'),
    path('tickets/my/', MyTicketsView.as_view(), name='my-tickets'),
]