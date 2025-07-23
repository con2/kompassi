import graphene
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from kompassi.core.utils.text_utils import normalize_whitespace
from kompassi.graphql_api.utils import resolve_local_datetime_field, resolve_localized_field, resolve_unix_seconds_field

from ..models import ScheduleItem


class LimitedScheduleItemType(DjangoObjectType):
    class Meta:
        model = ScheduleItem
        fields = (
            "slug",
            "start_time",
            "created_at",
            "updated_at",
            "cached_dimensions",
        )

    cached_dimensions = graphene.Field(GenericScalar)

    @staticmethod
    def resolve_duration_minutes(parent: ScheduleItem, info):
        return parent.duration.total_seconds() // 60

    duration_minutes = graphene.NonNull(graphene.Int)

    @staticmethod
    def resolve_length_minutes(parent: ScheduleItem, info):
        """
        Deprecated alias for `duration_minutes`.
        """
        return LimitedScheduleItemType.resolve_duration_minutes(parent, info)

    length_minutes = graphene.NonNull(
        graphene.Int,
        description=normalize_whitespace(resolve_length_minutes.__doc__ or ""),
    )

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

    @staticmethod
    def resolve_room(parent: ScheduleItem, info):
        """
        Convenience helper to get the value slug of the `room` dimension.
        NOTE: You should usually display `location` to users instead.
        """
        value_slugs = parent.cached_dimensions.get("room", [])
        return value_slugs[0] if value_slugs else ""

    room = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(resolve_room.__doc__ or ""),
    )

    @staticmethod
    def resolve_freeform_location(parent: ScheduleItem, info):
        """
        Convenience helper to get the freeform location of the schedule item.
        NOTE: You should usually display `location` to users instead.
        """
        return parent.annotations.get("internal:freeformLocation", "")

    freeform_location = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(resolve_freeform_location.__doc__ or ""),
    )

    @staticmethod
    def resolve_subtitle(parent: ScheduleItem, info):
        """
        Convenience helper to get the subtitle of the schedule item.
        NOTE: You should usually display `title` to users instead.
        """
        return parent.annotations.get("internal:subtitle", "")

    subtitle = graphene.NonNull(
        graphene.String,
        description=normalize_whitespace(resolve_subtitle.__doc__ or ""),
    )

    @staticmethod
    def resolve_is_cancelled(schedule_item: ScheduleItem, info):
        return schedule_item.is_cancelled

    is_cancelled = graphene.NonNull(graphene.Boolean)
