import django_filters
from events.models import Event

class EventFilter(django_filters.FilterSet):
    starts_from = django_filters.IsoDateTimeFilter(field_name='starts_at', lookup_expr='gte')
    starts_to = django_filters.IsoDateTimeFilter(field_name='starts_at', lookup_expr='lte')

    ends_from = django_filters.IsoDateTimeFilter(field_name='ends_at', lookup_expr='gte')
    ends_to = django_filters.IsoDateTimeFilter(field_name='ends_at', lookup_expr='lte')

    venue_type = django_filters.CharFilter(field_name='venue_type', lookup_expr='exact')

    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = Event
        fields = [
            'venue_type',
            'status',
        ]