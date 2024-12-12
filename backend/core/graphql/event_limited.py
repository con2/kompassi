from graphene_django import DjangoObjectType

from core.models import Event
from graphql_api.utils import resolve_local_datetime_field


class LimitedEventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = (
            "slug",
            "name",
            "start_time",
            "end_time",
            "timezone_name",
        )

    resolve_start_time = resolve_local_datetime_field("start_time")
    resolve_end_time = resolve_local_datetime_field("end_time")
