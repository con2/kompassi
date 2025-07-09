import graphene

from ..models import ScheduleItem
from .program_limited import LimitedProgramType
from .schedule_item_limited import LimitedScheduleItemType


class FullScheduleItemType(LimitedScheduleItemType):
    program = graphene.NonNull(LimitedProgramType)

    class Meta:
        model = ScheduleItem
        fields = (
            "program",
            "slug",
            "start_time",
            "created_at",
            "updated_at",
        )
