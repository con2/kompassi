import graphene
from graphene_django import DjangoObjectType

from core.models import Event
from forms.graphql.meta import FormsEventMetaType
from forms.models.meta import FormsEventMetaPlaceholder
from graphql_api.utils import resolve_local_datetime_field
from program_v2.graphql.meta import ProgramV2EventMetaType


class FullEventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = ("slug", "name", "start_time", "end_time", "timezone_name")

    program = graphene.Field(ProgramV2EventMetaType)

    @staticmethod
    def resolve_program(parent: Event, info):
        return parent.program_v2_event_meta

    forms = graphene.Field(FormsEventMetaType)

    @staticmethod
    def resolve_forms(event: Event, info):
        return FormsEventMetaPlaceholder(event)

    resolve_start_time = resolve_local_datetime_field("start_time")
    resolve_end_time = resolve_local_datetime_field("end_time")
