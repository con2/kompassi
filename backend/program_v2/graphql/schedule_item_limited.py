import graphene
from graphene_django import DjangoObjectType

from core.utils.text_utils import normalize_whitespace
from graphql_api.utils import resolve_local_datetime_field, resolve_localized_field, resolve_unix_seconds_field

from ..models import ScheduleItem


class LimitedScheduleItemType(DjangoObjectType):
    class Meta:
        model = ScheduleItem
        fields = (
            "slug",
            "subtitle",
            "start_time",
            "created_at",
            "updated_at",
        )

    @staticmethod
    def resolve_length_minutes(parent: ScheduleItem, info):
        return parent.length.total_seconds() // 60

    length_minutes = graphene.NonNull(graphene.Int)

    resolve_start_time = resolve_local_datetime_field("start_time")

    end_time = graphene.NonNull(graphene.DateTime)
    resolve_end_time = resolve_local_datetime_field("cached_end_time")

    start_time_unix_seconds = graphene.NonNull(graphene.Int)
    resolve_start_time_unix_seconds = resolve_unix_seconds_field("start_time")

    end_time_unix_seconds = graphene.NonNull(graphene.Int)
    resolve_end_time_unix_seconds = resolve_unix_seconds_field("end_time)")

    resolve_location = resolve_localized_field("cached_location")
    location = graphene.String(lang=graphene.String())

    resolve_created_at = resolve_local_datetime_field("created_at")
    resolve_updated_at = resolve_local_datetime_field("updated_at")

    @staticmethod
    def resolve_title(parent: ScheduleItem, info):
        """
        Returns the title of the program, with subtitle if it exists,
        in the format "Program title – Schedule item subtitle".
        """
        return parent.title

    title = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(resolve_title.__doc__ or ""),
    )
