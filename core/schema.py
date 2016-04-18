# encoding: utf-8

from __future__ import unicode_literals

from graphene import relay, ObjectType
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.contrib.django.types import DjangoNode

from .models import Event


class EventNode(DjangoNode):
    class Meta:
        model = Event
        filter_fields = ['slug']


class Query(ObjectType):
    event = relay.NodeField(EventNode)
    all_events = DjangoFilterConnectionField(EventNode)

    class Meta:
        abstract = True
