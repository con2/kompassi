from rest_framework import viewsets

from ..models import Event
from ..serializers import EventSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.filter(public=True)
    serializer_class = EventSerializer
    lookup_field = 'slug'
