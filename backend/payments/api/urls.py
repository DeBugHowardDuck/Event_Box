from django.urls import path
from .views import YooKassaCreatePaymentView
from payments.views import payment_return

urlpatterns = [
    path("payments/yookassa/create/", YooKassaCreatePaymentView.as_view(), name="yookassa-create-payment"),
    path("payments/return/", payment_return, name="payment-return"),
]
