import graphene
from graphene_django import DjangoObjectType

from core.models import Event
from forms.graphql.meta import FormsEventMetaType
from forms.models.meta import FormsEventMeta
from program_v2.graphql import ProgramV2EventMetaType


class FullEventType(DjangoObjectType):
    class Meta:
        model = Event

        # NOTE: NOTE: keep in sync with graphql_api/schema.py
        fields = ("slug", "name")

    program = graphene.Field(ProgramV2EventMetaType)

    @staticmethod
    def resolve_program(parent: Event, info):
        return parent.program_v2_event_meta

    forms = graphene.Field(FormsEventMetaType)

    @staticmethod
    def resolve_forms(event: Event, info):
        return FormsEventMeta(event)
