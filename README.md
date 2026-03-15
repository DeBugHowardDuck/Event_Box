# Event Box

Event Box — платформы мероприятий: организатор публикует событие и типы билетов, пользователь покупает билет и получает QR, на входе роль checker проверяет билет через check-in.

Стек: Django + DRF, PostgreSQL, Redis, Celery/Beat, drf-yasg (Swagger/Redoc), React + Vite + TypeScript + MUI.

---

## Возможности

### Публичная часть
- Каталог событий с пагинацией
- Страница события: описание + выбор билета и количества + покупка

### Пользователь (role=user)
- Регистрация / вход / выход
- Мои заказы (статусы)
- Мои билеты (QR)

### Организатор (role=organizer)
- Создание и публикация событий (draft → published)
- Управление типами билетов (TicketType): цена/квота/активность

### Checker (role=checker)
- Экран check-in: ввод/скан QR payload
- Проверка билета и перевод в USED (защита от повторного прохода)

### Оплата
- Создание платежа YooKassa и редирект на оплату
- Подтверждение оплаты по webhook.

### Фоновые задачи (Celery)
- Expire зависших оплат: pending_paid → expired по таймеру
- (опционально) отправка email после подтверждения оплаты, если настроено

---

## Скриншоты

Каталог событий  
![Catalog](docs/screenshots/1_events.png)

Страница события + покупка  
![Event detail](docs/screenshots/2_detail_events.png)

YooKassa checkout (тестовый)  
![YooKassa](docs/screenshots/3_peyment_test.png)

Успешная оплата (return page)  
![Payment success](docs/screenshots/5_peyment_test.png)

Мои заказы  
![My orders](docs/screenshots/6_orders_status.png)

Мои билеты (QR)  
![My tickets](docs/screenshots/7_tickets_status.png)

Checker (OK)  
![Checker ok](docs/screenshots/6_checker_qr.png)

Checker (already used)  
![Checker used](docs/screenshots/7_already_used_qr.png)

Swagger  
![Swagger](docs/screenshots/8_swagger.png)

Admin  
![Admin](docs/screenshots/9_admin.png)

Create event
![Create_event](docs/screenshots/10_my_event.png)

Create event main menu
![Create_event_main_menu](docs/screenshots/11_my_event.png)

Price tickets
![Price_tickets](docs/screenshots/12_price_tickets.png)

---

## Структура репозитория

- `backend/` — Django + DRF (API)
- `frontend/` — React + Vite + TypeScript (UI)
---

## Быстрый запуск (локально)

### Требования
- Python 3.11+
- Node.js 18+
- Docker Desktop

---

## 1) Запуск PostgreSQL и Redis

Из корня репозитория:

```bash

docker compose up -d
docker compose ps
```

## 2) Backend Django

### 2.1 Виртуальное окружение и зависимости

```bash

# из корня репозитория
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

### 2.2 Переменные окружения

Создай файл `.env` и укажи в нём значения:

```env
SECRET_KEY=your_secret_key

DATABASE_URL=postgresql://user:password@localhost:5432/event_box

REDIS_URL=redis://localhost:6379/0

YOOKASSA_SHOP_ID=your_shop_id

YOOKASSA_SECRET_KEY=your_secret_key

YOOKASSA_RETURN_URL=http://localhost:5173/payment/success
```

### 2.3 Миграции - админ - демо-данные

```bash

cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
```

### 2.4 Опубликовать демо-события

1. Откройте админку: `http://localhost:8000/admin/`
2. Перейдите в `Events → Event`
3. Откройте событие и установите статус `published`

### 2.5 Запуск сервера


```bash

cd backend
python manage.py runserver
```

#### Backend: http://localhost:8000

### 3) Celery (worker + beat)

### Worker (Windows-safe)

```bash

cd backend
celery -A config worker -l INFO --pool=solo
```

### Beat
```bash

cd backend
celery -A config beat -l INFO
```

### 4) Frontend
```bash

cd frontend
npm install
npm run dev
```

#### Frontend: http://localhost:5173

## Документация API

- Swagger: [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/)
- Redoc: [http://localhost:8000/api/docs/redoc/](http://localhost:8000/api/docs/redoc/)

## Роли и тестовые аккаунты

### user

Создаётся через регистрацию на фронте:

`http://localhost:5173/register`

### organizer / checker

Проще создавать через админку:

`http://localhost:8000/admin/` → `Users` → `Add`

У пользователя заполнить поле `role` (`organizer` или `checker`).

## Демонстрационный сценарий

**Организатор**

1. Войти как `organizer`
2. Создать событие → добавить `TicketType` → опубликовать
3. Убедиться, что событие появилось в каталоге (`published`)

**Пользователь**

1. Зарегистрироваться или войти
2. Открыть событие → купить билет → перейти в YooKassa → оплатить
3. Проверить разделы “Мои заказы” и “Мои билеты”

**Checker**

1. Войти как `checker`
2. Открыть `/checker`
3. Скопировать `qr_payload` из раздела “Мои билеты” у пользователя
4. Проверить билет: первый раз — `ok`, второй раз — `already_used`

## Вебхуки YooKassa

Подтверждение оплаты происходит по webhook. Редирект на `return_url` — это только возврат пользователя в приложение, но не подтверждение статуса заказа.

### Почему локально заказ может остаться `pending_paid`

YooKassa отправляет webhook на публичный HTTPS URL. `localhost` недоступен из интернета, поэтому webhook не приходит автоматически без туннеля или деплоя.

### Как проверить полный цикл локально


**Для локального демо:** симулировать подтверждение оплаты вручную через админку:

1. `Admin → Orders → Order` → поставить `status=paid`
2. `Admin → Orders → Ticket` → поставить `status=active`

После этого QR станет “активным”, и check-in будет работать.

