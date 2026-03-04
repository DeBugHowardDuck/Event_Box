from django.urls import path
from .views import YooKassaCreatePaymentView, YooKassaWebhookView
from payments.views import payment_return

urlpatterns = [
    path(
        "payments/yookassa/create/",
        YooKassaCreatePaymentView.as_view(),
        name="yookassa-create-payment",
    ),
    path("payments/return/", payment_return, name="payment-return"),
    path("payments/yookassa/create/", YooKassaCreatePaymentView.as_view(), name="yookassa-create-payment"),
    path("webhooks/yookassa/", YooKassaWebhookView.as_view(), name="yookassa-webhook"),
]
