from graphene_django import DjangoObjectType

from core.models import Event


class LimitedEventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = ("slug", "name")
