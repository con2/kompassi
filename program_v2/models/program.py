import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Optional

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, transaction

from core.models import Event
from core.utils import log_delete, log_get_or_create, validate_slug

if TYPE_CHECKING:
    from .dimension import ProgramDimensionValue


logger = logging.getLogger("kompassi")


class Program(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="programs")
    title = models.CharField(max_length=1023)
    slug = models.CharField(max_length=1023, validators=[validate_slug])
    description = models.TextField(blank=True)
    other_fields = models.JSONField(blank=True, default=dict)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # denormalized fields
    cached_dimensions = models.JSONField(default=dict)

    # related fields
    dimensions: models.QuerySet["ProgramDimensionValue"]

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
        for pdv in self.dimensions.all():
            dimensions[pdv.dimension.slug].append(pdv.value.slug)
        return dimensions

    @classmethod
    def refresh_cached_dimensions(cls, queryset: models.QuerySet["Program"]):
        for program in (
            queryset.select_for_update(of=("self",))
            .only("id", "cached_dimensions")
            .prefetch_related(
                "dimensions__dimension__slug",
                "dimensions__value__slug",
            )
        ):
            program.cached_dimensions = program._dimensions
            program.save(update_fields=["cached_dimensions"])

    @staticmethod
    def create_from_form_data(
        event: Event,
        values: dict[str, Any],
        created_by: Optional["User"] = None,
    ) -> "Program":
        """
        Given the responses from a program form, creates a new program.
        Basic fields such as title and description are populated from the form.
        Fields whose names match dimension names are assumed to be dimensions.
        All other fields are stored in other_fields.
        """
        from ..forms import ProgramForm
        from .dimension import DimensionValue, ProgramDimensionValue

        values = values.copy()

        with transaction.atomic():
            dimension_values: list[DimensionValue] = []
            for dimension in event.dimensions.all():
                # TODO multiple values per dimension
                dimension_value_slug = values.pop(dimension.slug, None)
                if dimension_value_slug is None:
                    continue

                dimension_value = DimensionValue.objects.get(dimension=dimension, slug=dimension_value_slug)
                dimension_values.append(dimension_value)

            program = ProgramForm(values).save(commit=False)
            program.event = event
            program.created_by = created_by

            for field_name in ProgramForm.Meta.fields:
                values.pop(field_name, None)

            program.other_fields = values
            program.save()

            for dimension_value in dimension_values:
                ProgramDimensionValue.objects.create(
                    program=program,
                    dimension=dimension_value.dimension,
                    value=dimension_value,
                )

        return program

    def update_from_form_data(self, values: dict[str, Any]):
        """
        Given the responses from a program form, updates the program.
        Matches semantics from create_from_form_data.

        NOTE: if you need the instance afterwards, use the returned one or do a refresh_from_db.
        """
        from ..forms import ProgramForm
        from .dimension import DimensionValue, ProgramDimensionValue

        values = values.copy()

        with transaction.atomic():
            for dimension in self.event.dimensions.all():
                # TODO multiple values per dimension
                dimension_value_slug = values.pop(dimension.slug, None)
                if dimension_value_slug is None:
                    continue

                dimension_value = DimensionValue.objects.get(dimension=dimension, slug=dimension_value_slug)

                ProgramDimensionValue.objects.filter(
                    program=self,
                    dimension=dimension,
                ).delete()
                ProgramDimensionValue.objects.create(
                    program=self,
                    dimension=dimension,
                    value=dimension_value,
                )

            program = ProgramForm(values, instance=self).save(commit=False)

            for field_name in ProgramForm.Meta.fields:
                values.pop(field_name, None)

            program.other_fields = values
            program.save()

        return program

    @classmethod
    def import_program_v1(cls, event: "Event", clear=False):
        from programme.models import Programme

        from .dimension import Dimension, DimensionValue, ProgramDimensionValue
        from .schedule import ScheduleItem

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
                        value=DimensionValue.objects.get(dimension=dimension, slug=v1_value.slug),
                    )
                    log_get_or_create(logger, pdv, created)
