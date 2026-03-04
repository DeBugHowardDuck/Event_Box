import uuid
from yookassa import Payment as YooPayment, Configuration


def configure_yookassa(shop_id: str, secret_key: str) -> None:
    Configuration.account_id = shop_id
    Configuration.secret_key = secret_key


def create_yookassa_payment(*, amount_value: str, currency: str, description: str, return_url: str, order_id: int):
    idempotence_key = str(uuid.uuid4())

    payload = {
        "amount": {"value": amount_value, "currency": currency},
        "capture": True,
        "confirmation": {"type": "redirect", "return_url": return_url},
        "description": description,
        "metadata": {"order_id": str(order_id)},
    }

    payment = YooPayment.create(payload, idempotence_key)
    return payment