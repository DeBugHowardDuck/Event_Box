import uuid

def make_ticket_payload(ticket_code: uuid.UUID) -> str:
    return f'event_box: {ticket_code}'