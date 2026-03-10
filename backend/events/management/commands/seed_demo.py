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
                "status": Event.Status.PUBLISHED,
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
                "status": Event.Status.PUBLISHED,
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
                "starts_at": now + timedelta(days=16),
                "ends_at": now + timedelta(days=16, hours=3),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Юсуповская 107",
                "status": Event.Status.PUBLISHED,
                "capacity": 50,
                "registration_ends_at": now + timedelta(days=15),
            },
        )

        TicketType.objects.get_or_create(
            event=event3,
            name="Входной билет",
            defaults={
                "price": "89.90",
                "currency": "RUB",
                "quota": 50,
                "sales_start": now,
                "sales_end": now + timedelta(days=15),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие четвертое офлайн.
        event4, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Мастеркласс по моделированию.",
            defaults={
                "description": "Соорудим свой собственный корабль.",
                "starts_at": now + timedelta(days=18),
                "ends_at": now + timedelta(days=18, hours=3),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Пугачева 48/29",
                "status": Event.Status.PUBLISHED,
                "capacity": 50,
                "registration_ends_at": now + timedelta(days=17),
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
                "sales_end": now + timedelta(days=17),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие пятое офлайн.
        event5, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Концерт Аллы Пугачевой.",
            defaults={
                "description": "Лучшие хиты всех времен!",
                "starts_at": now + timedelta(days=20),
                "ends_at": now + timedelta(days=20, hours=3),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Арсенальная набережная 91",
                "status": Event.Status.PUBLISHED,
                "capacity": 50,
                "registration_ends_at": now + timedelta(days=19),
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
                "sales_end": now + timedelta(days=19),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие шестое офлайн.
        event6, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Лекция по истории кино.",
            defaults={
                "description": "Разберем самые известные фильмы прошлого века.",
                "starts_at": now + timedelta(days=22),
                "ends_at": now + timedelta(days=22, hours=2),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Проспект Мира 12",
                "status": Event.Status.PUBLISHED,
                "capacity": 70,
                "registration_ends_at": now + timedelta(days=21),
            },
        )

        TicketType.objects.get_or_create(
            event=event6,
            name="Билет на лекцию",
            defaults={
                "price": "24.90",
                "currency": "RUB",
                "quota": 70,
                "sales_start": now,
                "sales_end": now + timedelta(days=21),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие седьмое онлайн.
        event7, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Онлайн воркшоп по Python.",
            defaults={
                "description": "Поговорим про основы Python и напишем немного кода.",
                "starts_at": now + timedelta(days=24),
                "ends_at": now + timedelta(days=24, hours=2),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.ONLINE,
                "online_url": "http://example.com/python-workshop",
                "status": Event.Status.PUBLISHED,
                "capacity": 120,
                "registration_ends_at": now + timedelta(days=23),
            },
        )

        TicketType.objects.get_or_create(
            event=event7,
            name="Онлайн билет",
            defaults={
                "price": "29.90",
                "currency": "RUB",
                "quota": 120,
                "sales_start": now,
                "sales_end": now + timedelta(days=23),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие восьмое офлайн.
        event8, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Фестиваль настольных игр.",
            defaults={
                "description": "Будем играть, общаться и весело проводить время.",
                "starts_at": now + timedelta(days=26),
                "ends_at": now + timedelta(days=26, hours=5),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Лесная 25",
                "status": Event.Status.PUBLISHED,
                "capacity": 90,
                "registration_ends_at": now + timedelta(days=25),
            },
        )

        TicketType.objects.get_or_create(
            event=event8,
            name="Входной билет",
            defaults={
                "price": "39.90",
                "currency": "RUB",
                "quota": 90,
                "sales_start": now,
                "sales_end": now + timedelta(days=25),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие девятое офлайн.
        event9, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Фотопрогулка по Москве.",
            defaults={
                "description": "Погуляем по красивым местам и сделаем атмосферные кадры.",
                "starts_at": now + timedelta(days=28),
                "ends_at": now + timedelta(days=28, hours=3),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Никольская 7",
                "status": Event.Status.PUBLISHED,
                "capacity": 25,
                "registration_ends_at": now + timedelta(days=27),
            },
        )

        TicketType.objects.get_or_create(
            event=event9,
            name="Участие в прогулке",
            defaults={
                "price": "34.90",
                "currency": "RUB",
                "quota": 25,
                "sales_start": now,
                "sales_end": now + timedelta(days=27),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие десятое онлайн.
        event10, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Вебинар по тайм-менеджменту.",
            defaults={
                "description": "Разберем, как все успевать и не выгорать.",
                "starts_at": now + timedelta(days=30),
                "ends_at": now + timedelta(days=30, hours=2),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.ONLINE,
                "online_url": "http://example.com/time-management",
                "status": Event.Status.PUBLISHED,
                "capacity": 200,
                "registration_ends_at": now + timedelta(days=29),
            },
        )

        TicketType.objects.get_or_create(
            event=event10,
            name="Доступ к вебинару",
            defaults={
                "price": "15.00",
                "currency": "RUB",
                "quota": 200,
                "sales_start": now,
                "sales_end": now + timedelta(days=29),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие одиннадцатое офлайн.
        event11, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Ярмарка локальных брендов.",
            defaults={
                "description": "Одежда, украшения и товары ручной работы.",
                "starts_at": now + timedelta(days=32),
                "ends_at": now + timedelta(days=32, hours=6),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Хлебозавод 9",
                "status": Event.Status.PUBLISHED,
                "capacity": 300,
                "registration_ends_at": now + timedelta(days=31),
            },
        )

        TicketType.objects.get_or_create(
            event=event11,
            name="Гостевой билет",
            defaults={
                "price": "10.00",
                "currency": "RUB",
                "quota": 300,
                "sales_start": now,
                "sales_end": now + timedelta(days=31),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие двенадцатое офлайн.
        event12, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Интенсив по публичным выступлениям.",
            defaults={
                "description": "Попрактикуемся говорить уверенно и без страха.",
                "starts_at": now + timedelta(days=34),
                "ends_at": now + timedelta(days=34, hours=4),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Тверская 18",
                "status": Event.Status.PUBLISHED,
                "capacity": 45,
                "registration_ends_at": now + timedelta(days=33),
            },
        )

        TicketType.objects.get_or_create(
            event=event12,
            name="Билет участника",
            defaults={
                "price": "49.90",
                "currency": "RUB",
                "quota": 45,
                "sales_start": now,
                "sales_end": now + timedelta(days=33),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие тринадцатое офлайн.
        event13, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Кулинарный вечер итальянской кухни.",
            defaults={
                "description": "Приготовим пасту и десерт вместе с шефом.",
                "starts_at": now + timedelta(days=36),
                "ends_at": now + timedelta(days=36, hours=3),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Садовая-Каретная 20",
                "status": Event.Status.PUBLISHED,
                "capacity": 25,
                "registration_ends_at": now + timedelta(days=35),
            },
        )

        TicketType.objects.get_or_create(
            event=event13,
            name="Место на кухне",
            defaults={
                "price": "79.90",
                "currency": "RUB",
                "quota": 25,
                "sales_start": now,
                "sales_end": now + timedelta(days=35),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие четырнадцатое офлайн.
        event14, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Ночь научного кино.",
            defaults={
                "description": "Посмотрим документальные фильмы о науке и технологиях.",
                "starts_at": now + timedelta(days=38),
                "ends_at": now + timedelta(days=38, hours=4),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.OFFLINE,
                "venue_address": "Москва, Ленинский проспект 62",
                "status": Event.Status.PUBLISHED,
                "capacity": 70,
                "registration_ends_at": now + timedelta(days=37),
            },
        )

        TicketType.objects.get_or_create(
            event=event14,
            name="Кинобилет",
            defaults={
                "price": "17.50",
                "currency": "RUB",
                "quota": 70,
                "sales_start": now,
                "sales_end": now + timedelta(days=37),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))

        # Мероприятие пятнадцатое онлайн.
        event15, _ = Event.objects.get_or_create(
            organizer=organizer,
            title="Онлайн Q&A с разработчиком.",
            defaults={
                "description": "Ответы на вопросы про карьеру, код и первые проекты.",
                "starts_at": now + timedelta(days=40),
                "ends_at": now + timedelta(days=40, hours=2),
                "timezone": "Europe/Moscow",
                "venue_type": Event.VenueType.ONLINE,
                "online_url": "http://example.com/dev-qa",
                "status": Event.Status.PUBLISHED,
                "capacity": 150,
                "registration_ends_at": now + timedelta(days=39),
            },
        )

        TicketType.objects.get_or_create(
            event=event15,
            name="Доступ к эфиру",
            defaults={
                "price": "12.90",
                "currency": "RUB",
                "quota": 150,
                "sales_start": now,
                "sales_end": now + timedelta(days=39),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демка создана."))