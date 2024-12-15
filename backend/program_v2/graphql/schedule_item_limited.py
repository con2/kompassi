import graphene
from graphene_django import DjangoObjectType

from core.utils.text_utils import normalize_whitespace
from graphql_api.language import DEFAULT_LANGUAGE
from graphql_api.utils import (
    resolve_local_datetime_field,
    resolve_localized_field,
    resolve_localized_field_getattr,
)

from ..models import ScheduleItem


class LimitedScheduleItemType(DjangoObjectType):
    class Meta:
        model = ScheduleItem
        fields = (
            "slug",
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

    resolve_location = resolve_localized_field("cached_location")
    location = graphene.String(lang=graphene.String())

    resolve_created_at = resolve_local_datetime_field("created_at")
    resolve_updated_at = resolve_local_datetime_field("updated_at")

    @staticmethod
    def resolve_title(schedule_item: ScheduleItem, info, lang: str = DEFAULT_LANGUAGE):
        """
        Returns the title of the program, with subtitle if it exists,
        in the format "Program title – Schedule item subtitle".
        """
        return schedule_item.get_title(lang)

    title = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(resolve_title.__doc__ or ""),
    )

    subtitle = graphene.NonNull(
        graphene.String,
        description="Subtitle of the schedule item.",
    )
    resolve_subtitle = resolve_localized_field_getattr("subtitle")
