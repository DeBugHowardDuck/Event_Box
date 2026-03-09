from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from events.models import Event, TicketType


class Command(BaseCommand):
    help = "Create demo organizer + demo events and ticket types."

    def handle(self, *args, **options):
        User = get_user_model()

        organizer, created = User.objects.get_or_create(
            email="organizer_2@example.com",
            defaults={
                "role": "organizer",
                "is_active": True,
            },
        )
        if created:
            organizer.set_password("organizer1234")
            organizer.save()
            self.stdout.write(
                self.style.SUCCESS("Создан organizer@example.com / organizer123")
            )
        else:
            self.stdout.write("Организатор уже существует.")

        now = timezone.now()

        # Мероприятие 1 - онлайн.
        event1, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Онлайн встреча читателей.",
            defaults={
                "description": "Демка онлайн мероприятия.",
                "starts_at": now + timedelta(days=7),
                "ends_at": now + timedelta(days=7, hours=2),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.ONLINE,
                "online_url": "http://example.com/event",
                "status": Event.Status.DRAFT,
                "capacity": 100,
                "registration_ends_at": now + timedelta(days=6, hours=23),
            },
        )

        TicketType.objects.get_or_create(
            event=event1,
            name="Standard",
            defaults={
                "price": "9.99",
                "currency": "RUB",
                "quota": 80,
                "sales_start": now,
                "sales_end": now + timedelta(days=6),
                "is_active": True,
            },
        )

        TicketType.objects.get_or_create(
            event=event1,
            name="VIP",
            defaults={
                "price": "19.99",
                "currency": "RUB",
                "quota": 20,
                "sales_start": now,
                "sales_end": now + timedelta(days=6),
                "is_active": True,
            },
        )

        # Мероприятие второе офлайн.
        event2, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Проезд на пароме.",
            defaults={
                "description": "Прокатимся на пароме.",
                "starts_at": now + timedelta(days=14),
                "ends_at": now + timedelta(days=14, hours=3),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Андреевская 96/3",
                "status": Event.Status.DRAFT,
                "capacity": 50,
                "registration_ends_at": now + timedelta(days=13),
            },
        )

        TicketType.objects.get_or_create(
            event=event2,
            name="Место на палубе",
            defaults={
                "price": "14.90",
                "currency": "RUB",
                "quota": 50,
                "sales_start": now,
                "sales_end": now + timedelta(days=13),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))


        # Мероприятие третье офлайн.

        event3, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Читательский клуб.",
            defaults={
                "description": "Почитаем очень интересненькое",
                "starts_at": now + timedelta(days=14),
                "ends_at": now + timedelta(days=14, hours=3),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Юсуповская 107",
                "status": Event.Status.DRAFT,
                "capacity": 50,
                "registration_ends_at": now + timedelta(days=13),
            },
        )

        TicketType.objects.get_or_create(
            event=event3,
            name="Место на палубе",
            defaults={
                "price": "89.90",
                "currency": "RUB",
                "quota": 50,
                "sales_start": now,
                "sales_end": now + timedelta(days=13),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие четвертое офлайн.

        event4, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Мастекласс по моделированию.",
            defaults={
                "description": "Соорудим свой собственный корабль.",
                "starts_at": now + timedelta(days=14),
                "ends_at": now + timedelta(days=14, hours=3),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Пугачева 48/29",
                "status": Event.Status.DRAFT,
                "capacity": 50,
                "registration_ends_at": now + timedelta(days=13),
            },
        )

        TicketType.objects.get_or_create(
            event=event4,
            name="Место в зале.",
            defaults={
                "price": "102.90",
                "currency": "RUB",
                "quota": 50,
                "sales_start": now,
                "sales_end": now + timedelta(days=13),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие пятое офлайн.

        event5, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Концерт Аллы Пугачевы",
            defaults={
                "description": "Лучшие хиты всех времен!",
                "starts_at": now + timedelta(days=14),
                "ends_at": now + timedelta(days=14, hours=3),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Арсенальная набержная 91",
                "status": Event.Status.DRAFT,
                "capacity": 50,
                "registration_ends_at": now + timedelta(days=13),
            },
        )

        TicketType.objects.get_or_create(
            event=event5,
            name="Место в зале",
            defaults={
                "price": "65.70",
                "currency": "RUB",
                "quota": 50,
                "sales_start": now,
                "sales_end": now + timedelta(days=13),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))
