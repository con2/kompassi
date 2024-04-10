import graphene
from graphene_django import DjangoObjectType

from ..models import (
    ScheduleItem,
)


class ScheduleItemType(DjangoObjectType):
    class Meta:
        model = ScheduleItem
        fields = ("subtitle", "start_time")

    @staticmethod
    def resolve_length_minutes(parent: ScheduleItem, info):
        return parent.length.total_seconds() // 60

    length_minutes = graphene.NonNull(graphene.Int)

    @staticmethod
    def resolve_end_time(parent: ScheduleItem, info):
        return parent.end_time

    end_time = graphene.NonNull(graphene.DateTime)

    @staticmethod
    def resolve_start_time_unix_seconds(parent: ScheduleItem, info):
        return int(parent.start_time.timestamp())

    start_time_unix_seconds = graphene.NonNull(graphene.Int)

    @staticmethod
    def resolve_end_time_unix_seconds(parent: ScheduleItem, info):
        return int(parent.end_time.timestamp())

    end_time_unix_seconds = graphene.NonNull(graphene.Int)
