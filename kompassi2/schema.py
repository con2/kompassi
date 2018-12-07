from graphene_django import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene import Schema, Node, ObjectType

from core.models import Event


class EventNode(DjangoObjectType):
    class Meta:
        model = Event
        interfaces = (Node, )
        filter_fields = {
            "start_time": ["gte"],
            "end_time": ["lt"],
        }


class Query(ObjectType):
    event = Node.Field(EventNode)
    all_events = DjangoFilterConnectionField(EventNode)


schema = Schema(query=Query)
