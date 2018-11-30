from graphene_django import DjangoObjectType
import graphene

from core.models import Event as EventModel


class Event(DjangoObjectType):
    class Meta:
        model = EventModel


class Query(graphene.ObjectType):
    events = graphene.List(Event)

    @graphene.resolve_only_args
    def resolve_events(self):
        return EventModel.objects.all()


schema = graphene.Schema(query=Query)
