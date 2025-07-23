import graphene
from graphene_django import DjangoObjectType

from kompassi.core.models import Event
from kompassi.graphql_api.utils import resolve_local_datetime_field


class LimitedEventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = (
            "slug",
            "name",
            "start_time",
            "end_time",
        )

    resolve_start_time = resolve_local_datetime_field("start_time")
    resolve_end_time = resolve_local_datetime_field("end_time")

    @staticmethod
    def resolve_timezone(event: Event, info):
        """
        Eg. Europe/Helsinki.
        """
        return event.timezone_name

    timezone = graphene.NonNull(graphene.String)
