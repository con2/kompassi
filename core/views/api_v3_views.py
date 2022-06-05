from rest_framework import viewsets
from rest_framework.decorators import action

from ..models import Event
from ..serializers import EventSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.filter(public=True)
    serializer_class = EventSerializer
    lookup_field = "slug"

    @action(detail=True, methods=["get", "post"])
    def badges(self, **TODO):
        pass
