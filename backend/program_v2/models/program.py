from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Self

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, transaction
from django.http import HttpRequest
from django.urls import reverse

from core.models import Event
from core.utils import validate_slug
from core.utils.locale_utils import get_message_in_language
from graphql_api.language import DEFAULT_LANGUAGE

if TYPE_CHECKING:
    from programme.models.programme import Programme

    from .dimension import ProgramDimensionValue
    from .meta import ProgramV2EventMeta
    from .schedule import ScheduleItem


logger = logging.getLogger("kompassi")


class Program(models.Model):
    id: int

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="programs")
    title = models.CharField(max_length=1023)
    slug = models.CharField(max_length=1023, validators=[validate_slug])
    description = models.TextField(blank=True)
    other_fields = models.JSONField(blank=True, default=dict)

    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="favorite_programs", blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # denormalized fields
    cached_dimensions = models.JSONField(default=dict)
    cached_earliest_start_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "The earliest start time of any schedule item of this program. "
            "NOTE: This is not the same as the program's start time. "
            "The intended purpose of this field is to exclude programs that have not yet started. "
            "Always use `scheduleItems` for the purpose of displaying program times."
        ),
    )
    cached_latest_end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "The latest end time of any schedule item of this program. "
            "NOTE: This is not the same as the program's start end. "
            "The intended purpose of this field is to exclude programs that have already ended. "
            "Always use `scheduleItems` for the purpose of displaying program times."
        ),
    )

    # related fields
    dimensions: models.QuerySet[ProgramDimensionValue]
    schedule_items: models.QuerySet[ScheduleItem]

    class Meta:
        unique_together = ("event", "slug")

    def __str__(self):
        return str(self.title)

    def refresh_cached_fields(self):
        self.refresh_cached_dimensions()
        self.refresh_cached_times()

    @classmethod
    def refresh_cached_fields_qs(cls, queryset: models.QuerySet[Self]):
        cls.refresh_cached_dimensions_qs(queryset)
        cls.refresh_cached_times_qs(queryset)

    def _build_dimensions(self):
        """
        Used to populate cached_dimensions
        """
        # TODO should all event dimensions always be present, or only those with values?
        # TODO when dimensions are changed for an event, refresh all cached_dimensions
        dimensions = {dimension.slug: [] for dimension in self.event.dimensions.all()}
        for pdv in self.dimensions.all():
            dimensions[pdv.dimension.slug].append(pdv.value.slug)
        return dimensions

    def refresh_cached_dimensions(self):
        self.cached_dimensions = self._build_dimensions()
        self.save(update_fields=["cached_dimensions"])

    @classmethod
    def refresh_cached_dimensions_qs(cls, queryset: models.QuerySet[Self]):
        with transaction.atomic():
            bulk_update = []
            for program in queryset.select_for_update(of=("self",)).only("id", "cached_dimensions"):
                program.cached_dimensions = program._build_dimensions()
                bulk_update.append(program)
            cls.objects.bulk_update(bulk_update, ["cached_dimensions"])

    def refresh_cached_times(self):
        """
        Used to populate cached_earliest_start_time and cached_latest_end_time
        """
        earliest_start_time = self.schedule_items.order_by("start_time").first()
        latest_end_time = self.schedule_items.order_by("cached_end_time").last()

        self.cached_earliest_start_time = earliest_start_time.start_time if earliest_start_time else None
        self.cached_latest_end_time = latest_end_time.cached_end_time if latest_end_time else None

        self.save(update_fields=["cached_earliest_start_time", "cached_latest_end_time"])

    @classmethod
    def refresh_cached_times_qs(cls, queryset: models.QuerySet[Self]):
        with transaction.atomic():
            bulk_update = []
            for program in queryset.select_for_update(of=("self",)).only(
                "id",
                "cached_earliest_start_time",
                "cached_latest_end_time",
            ):
                earliest_start_time = program.schedule_items.order_by("start_time").first()
                latest_end_time = program.schedule_items.order_by("cached_end_time").last()

                program.cached_earliest_start_time = earliest_start_time.start_time if earliest_start_time else None
                program.cached_latest_end_time = latest_end_time.cached_end_time if latest_end_time else None

                bulk_update.append(program)

            cls.objects.bulk_update(bulk_update, ["cached_earliest_start_time", "cached_latest_end_time"])

    @classmethod
    def create_from_form_data(
        cls,
        event: Event,
        values: dict[str, Any],
        created_by: User | None = None,
    ) -> Self:
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
    def import_program_from_v1(
        cls,
        event: Event,
        queryset: models.QuerySet[Programme] | None = None,
        clear: bool = False,
    ):
        from programme.models.programme import Programme

        from .dimension import DimensionValue

        if (meta := event.program_v2_event_meta) is None:
            raise ValueError(f"Event {event.slug} does not have program_v2_event_meta")

        if queryset is None:
            queryset = Programme.objects.filter(category__event=event)

        if clear:
            cls.objects.filter(event=event).delete()
            DimensionValue.objects.filter(dimension__event=event).delete()
        else:
            slugs_to_delete = queryset.exclude(state="published").values_list("slug", flat=True)
            cls.objects.filter(event=event, slug__in=slugs_to_delete).delete()

        # Only imports published programme for now as there is no access control
        programs_to_upsert = queryset.filter(state="published")

        import_function = meta.importer
        import_function(event, programs_to_upsert)

    @property
    def meta(self) -> ProgramV2EventMeta:
        if (meta := self.event.program_v2_event_meta) is None:
            raise TypeError(f"Event {self.event.slug} does not have program_v2_event_meta but Programs are present")

        return meta

    def get_location(self, language=DEFAULT_LANGUAGE):
        """
        TODO(#474) Support freeform location
        https://github.com/con2/kompassi/issues/474
        """
        dimension = self.meta.location_dimension
        if dimension is None:
            return None

        pdv = self.dimensions.filter(dimension=dimension).first()
        if pdv is None:
            return None

        return get_message_in_language(pdv.value.title, language)

    def get_calendar_export_link(self, request: HttpRequest):
        return request.build_absolute_uri(
            reverse(
                "program_v2:single_program_calendar_export_view",
                kwargs=dict(
                    event_slug=self.event.slug,
                    program_slug=self.slug,
                ),
            )
        )
