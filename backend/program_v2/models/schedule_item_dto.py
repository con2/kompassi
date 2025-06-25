from datetime import datetime, timedelta

import pydantic

from core.utils.model_utils import slugify

from .program import Program
from .schedule_item import ScheduleItem


class ScheduleItemDTO(pydantic.BaseModel, populate_by_name=True, frozen=True):
    slug: str
    subtitle: str
    start_time: datetime = pydantic.Field(validation_alias="startTime")
    duration_minutes: int = pydantic.Field(validation_alias="lengthMinutes")
    room: str = pydantic.Field(default="")
    freeform_location: str = pydantic.Field(validation_alias="freeformLocation", default="")

    @property
    def duration(self) -> timedelta:
        return timedelta(minutes=self.duration_minutes)

    def save(self, program: Program) -> ScheduleItem:
        slug = slugify(self.slug)

        schedule_item = (
            ScheduleItem.objects.select_for_update(of=("self",), no_key=True)
            .filter(
                program=program,
                slug=slug,
            )
            .first()
        )

        if schedule_item is not None:
            schedule_item.start_time = self.start_time
            schedule_item.duration = self.duration
            schedule_item.annotations.update(
                {
                    "internal:subtitle": self.subtitle,
                    "internal:freeformLocation": self.freeform_location,
                }
            )
        else:
            schedule_item = ScheduleItem(
                program=program,
                slug=slug,
                start_time=self.start_time,
                duration=timedelta(minutes=self.duration_minutes),
                annotations={
                    "internal:subtitle": self.subtitle,
                    "internal:freeformLocation": self.freeform_location,
                },
            )

        schedule_item.with_mandatory_fields().save()
        schedule_item.set_dimension_values(
            {
                "room": [self.room] if self.room else [],
            },
            cache=program.meta.universe.preload_dimensions(dimension_slugs=["room"]),
        )
        schedule_item.refresh_cached_fields()
        schedule_item.refresh_dependents()

        return schedule_item
