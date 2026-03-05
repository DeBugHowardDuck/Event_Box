from datetime import timedelta
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

from events.models import Event
from orders.models import Order


@shared_task
def close_expired_registrations():
    now = timezone.now()
    return Event.objects.filter(registration_ends_at__isnull=False, registration_ends_at__lte=now).count()


@shared_task
def expire_pending_payments():
    minutes = settings.PENDING_PAYMENT_EXPIRE_MINUTES
    deadline = timezone.now() - timedelta(minutes=minutes)

    qs = Order.objects.filter(status=Order.Status.PENDING_PAID, created_at__lte=deadline)
    updated = qs.update(status=Order.Status.EXPIRED)
    return updated


@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    deadline = timezone.now() - timedelta(days=30)
    qs = User.objects.filter(is_active=True, last_login__isnull=False, last_login__lte=deadline)
    updated = qs.update(is_active=False)
    return updated


@shared_task
def ping():
    return "pong"
