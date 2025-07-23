from graphene_django import DjangoObjectType

from kompassi.core.models import Event


class LimitedEventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = ("slug", "name")
