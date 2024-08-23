import graphene
from graphene_django import DjangoObjectType

from core.utils.text_utils import normalize_whitespace
from graphql_api.utils import resolve_localized_field

from ..models import ScheduleItem


class LimitedScheduleItemType(DjangoObjectType):
    class Meta:
        model = ScheduleItem
        fields = ("slug", "subtitle", "start_time")

    @staticmethod
    def resolve_length_minutes(parent: ScheduleItem, info):
        return parent.length.total_seconds() // 60

    length_minutes = graphene.NonNull(graphene.Int)

    @staticmethod
    def resolve_end_time(parent: ScheduleItem, info):
        return parent.cached_end_time

    end_time = graphene.NonNull(graphene.DateTime)

    @staticmethod
    def resolve_start_time_unix_seconds(parent: ScheduleItem, info):
        return int(parent.start_time.timestamp())

    start_time_unix_seconds = graphene.NonNull(graphene.Int)

    @staticmethod
    def resolve_end_time_unix_seconds(parent: ScheduleItem, info):
        return int(parent.cached_end_time.timestamp())

    end_time_unix_seconds = graphene.NonNull(graphene.Int)

    resolve_location = resolve_localized_field("cached_location")
    location = graphene.String(lang=graphene.String())

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
