from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from orders.models import Order


@shared_task(bind=True, max_retries=3, default_retry_delay=30)
def send_paid_order_email(self, order_id: int):
    """
    Письмо пользователю после оплаты.
    Сейчас console backend → письмо увидишь в терминале.
    """
    try:
        order = Order.objects.select_related("user").get(id=order_id)
    except Order.DoesNotExist:
        return

    if order.status != Order.Status.PAID:
        return

    subject = f"EventBox: заказ #{order.id} оплачен"
    message = f"Оплата подтверждена. Кол-во билетов: {order.tickets.count()}"
    recipient = [order.user.email]

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient)