import logging
from datetime import timedelta
from typing import TYPE_CHECKING

from django.db import models

from core.utils import log_get_or_create, log_delete, validate_slug

from ..consts import TAG_DIMENSION_TITLE_LOCALIZED, CATEGORY_DIMENSION_TITLE_LOCALIZED

if TYPE_CHECKING:
    from core.models import Event
    from .dimension import ProgramDimensionValue


logger = logging.getLogger("kompassi")


class Program(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="programs")
    title = models.CharField(max_length=1023)
    slug = models.CharField(max_length=1023, validators=[validate_slug])
    description = models.TextField(blank=True)
    other_fields = models.JSONField(blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # denormalized fields
    cached_dimensions = models.JSONField(default=dict)

    # related fields
    program_dimension_values: models.QuerySet["ProgramDimensionValue"]

    class Meta:
        unique_together = ("event", "slug")

    def __str__(self):
        return str(self.title)

    @property
    def _dimensions(self):
        """
        Used to populate cached_dimensions
        """
        # TODO should all event dimensions always be present, or only those with values?
        # TODO when dimensions are changed for an event, refresh all cached_dimensions
        dimensions = {dimension.slug: [] for dimension in self.event.dimensions.all()}
        for pdv in self.program_dimension_values.all():
            dimensions[pdv.dimension.slug].append(pdv.dimension_value.slug)
        return dimensions

    @classmethod
    def refresh_cached_dimensions(cls, queryset: models.QuerySet["Program"]):
        for program in (
            queryset.select_for_update(of=("self",))
            .only("id", "cached_dimensions")
            .prefetch_related(
                "program_dimension_values__dimension__slug",
                "program_dimension_values__dimension_value__slug",
            )
        ):
            program.cached_dimensions = program._dimensions
            program.save(update_fields=["cached_dimensions"])

    @classmethod
    def import_program_v1(cls, event: "Event", clear=False):
        from . import Dimension, DimensionValue, ProgramDimensionValue, ScheduleItem
        from programme.models import Programme

        if clear:
            log_delete(logger, cls.objects.filter(event=event).delete())

        category_dimension, room_dimension, tag_dimension = Dimension.ensure_v1_default_dimensions(
            event,
            clear=clear,
        )

        for v1_program in Programme.objects.filter(category__event=event):
            program, created = cls.objects.get_or_create(
                event=event,
                slug=v1_program.slug,
                defaults=dict(
                    title=v1_program.title,
                    description=v1_program.description,
                ),
            )
            log_get_or_create(logger, program, created)

            if v1_program.start_time and v1_program.length:
                schedule_item, created = ScheduleItem.objects.get_or_create(
                    program=program,
                    defaults=dict(
                        start_time=v1_program.start_time,
                        length=timedelta(minutes=v1_program.length),
                    ),
                )
                log_get_or_create(logger, schedule_item, created)

            for dimension, queryset in [
                (category_dimension, [v1_program.category]),
                (room_dimension, [v1_program.room] if v1_program.room else []),
                (tag_dimension, v1_program.tags.all()),
            ]:
                for v1_value in queryset:
                    log_delete(
                        logger,
                        ProgramDimensionValue.objects.filter(dimension=dimension, program=program).delete(),
                    )
                    pdv, created = ProgramDimensionValue.objects.get_or_create(
                        program=program,
                        dimension=dimension,
                        dimension_value=DimensionValue.objects.get(dimension=dimension, slug=v1_value.slug),
                    )
                    log_get_or_create(logger, pdv, created)
