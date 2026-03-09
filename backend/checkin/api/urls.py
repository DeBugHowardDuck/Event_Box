from django.urls import path
from .views import CheckInQRView

urlpatterns = [
    path('checkin/qr/', CheckInQRView.as_view(), name='checkin-qr'),
]