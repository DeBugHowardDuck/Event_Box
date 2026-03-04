import hashlib
from django.core.cache import cache

EVENTS_VERSION_KEY = "events:version"


def get_events_version() -> int:
    v = cache.get(EVENTS_VERSION_KEY)
    if v is None:
        v = 1
        cache.set(EVENTS_VERSION_KEY, v, timeout=None)
    return int(v)


def bump_events_version() -> int:
    v = get_events_version() + 1
    cache.set(EVENTS_VERSION_KEY, v, timeout=None)
    return v


def make_query_hash(query_params) -> str:
    items = sorted((k, tuple(query_params.getlist(k))) for k in query_params.keys())
    raw = str(items).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def events_list_key(query_params) -> str:
    version = get_events_version()
    qh = make_query_hash(query_params)
    return f"events:list:v{version}:{qh}"


def events_detail_key(event_id: int) -> str:
    version = get_events_version()
    return f"events:detail:v{version}:{event_id}"
