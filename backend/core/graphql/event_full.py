import graphene

from core.models import Event
from forms.graphql.meta import FormsEventMetaType
from forms.models.meta import FormsEventMetaPlaceholder
from involvement.graphql.meta import InvolvementEventMetaType
from involvement.models.meta import InvolvementEventMeta
from program_v2.graphql.meta import ProgramV2EventMetaType
from tickets_v2.graphql.meta import TicketsV2EventMetaType

from .event_limited import LimitedEventType


class FullEventType(LimitedEventType):
    class Meta:
        model = Event
        fields = (
            "slug",
            "name",
            "start_time",
            "end_time",
            "timezone_name",
        )

    program = graphene.Field(ProgramV2EventMetaType)

    @staticmethod
    def resolve_program(parent: Event, info):
        return parent.program_v2_event_meta

    forms = graphene.Field(FormsEventMetaType)

    @staticmethod
    def resolve_forms(event: Event, info):
        return FormsEventMetaPlaceholder(event)

    tickets = graphene.Field(TicketsV2EventMetaType)

    @staticmethod
    def resolve_tickets(event: Event, info):
        return event.tickets_v2_event_meta

    involvement = graphene.Field(InvolvementEventMetaType)

    @staticmethod
    def resolve_involvement(event: Event, info):
        return InvolvementEventMeta(event)
