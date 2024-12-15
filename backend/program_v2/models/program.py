from __future__ import annotations

import logging
from datetime import tzinfo
from functools import cached_property
from typing import TYPE_CHECKING, Self

from django.conf import settings
from django.db import models, transaction
from django.http import HttpRequest
from django.urls import reverse
from django.utils.timezone import now

from core.models import Event
from core.utils import validate_slug

if TYPE_CHECKING:
    from programme.models.programme import Programme

    from .dimension_values import ProgramDimensionValue
    from .meta import ProgramV2EventMeta
    from .schedule import ScheduleItem


logger = logging.getLogger("kompassi")


class Program(models.Model):
    id: int

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="programs")

    # NOTE SUPPORTED_LANGUAGES
    title_fi = models.TextField(blank=True, default="")
    title_en = models.TextField(blank=True, default="")
    title_sv = models.TextField(blank=True, default="")

    slug = models.CharField(max_length=1023, validators=[validate_slug])

    # NOTE SUPPORTED_LANGUAGES
    description_fi = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_sv = models.TextField(blank=True)
    annotations = models.JSONField(blank=True, default=dict)

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
    cached_location = models.JSONField(blank=True, default=dict)
    cached_color = models.CharField(max_length=15, blank=True, default="")

    # related fields
    dimensions: models.QuerySet[ProgramDimensionValue]
    schedule_items: models.QuerySet[ScheduleItem]
    event_id: int

    class Meta:
        unique_together = ("event", "slug")

    def __str__(self):
        return str(self.title_fi)

    def _build_dimensions(self):
        dimensions = {dimension.slug: [] for dimension in self.event.program_universe.dimensions.all()}
        for pdv in self.dimensions.all():
            dimensions[pdv.value.dimension.slug].append(pdv.value.slug)
        return dimensions

    def _get_color(self):
        """
        Gets a color for the program from its dimension values.
        TODO deterministic behaviour when multiple colors are present (ordering for dimensions/values?)
        TODO move to scheduleItem?
        """
        first_pdv_with_color = self.dimensions.exclude(value__color="").first()
        return first_pdv_with_color.value.color if first_pdv_with_color else ""

    def _build_location(self):
        return ", ".join(set(self.schedule_items.all().values_list("cached_location", flat=True)))

    def with_generated_fields(self):
        self.cached_dimensions = self._build_dimensions()
        self.cached_location = self._build_location()
        self.cached_color = self._get_color()

        earliest_start_time = self.schedule_items.order_by("start_time").first()
        latest_end_time = self.schedule_items.order_by("cached_end_time").last()

        self.cached_earliest_start_time = earliest_start_time.start_time if earliest_start_time else None
        self.cached_latest_end_time = latest_end_time.cached_end_time if latest_end_time else None

        return self

    batch_size = 100
    cached_fields_from_dimensions = [
        "cached_dimensions",
        "cached_color",
        "updated_at",
    ]
    cached_fields_from_schedule_items = [
        "cached_earliest_start_time",
        "cached_latest_end_time",
        "updated_at",
    ]
    fields_needed_by_generated_fields = [
        "id",
        "cached_dimensions",
        "cached_color",
        "cached_earliest_start_time",
        "cached_latest_end_time",
    ]

    def refresh_cached_dimensions(self):
        self.with_generated_fields().save(update_fields=self.cached_fields_from_dimensions)

    @classmethod
    def refresh_cached_dimensions_qs(cls, queryset: models.QuerySet[Self]):
        """
        NOTE: Schedule items' cached dimensions depend on these.
        The caller is responsible for also calling ScheduleItem.refresh_cached_dimensions_qs.
        """
        with transaction.atomic():
            num_programs_updated = cls.objects.bulk_update(
                [
                    program.with_generated_fields()
                    for program in queryset.select_for_update(of=("self",)).only(
                        *cls.fields_needed_by_generated_fields,
                    )
                ],
                cls.cached_fields_from_dimensions,
                batch_size=cls.batch_size,
            )
            logger.info("Refreshed cached dimensions for %s programs", num_programs_updated)

    def refresh_cached_fields_from_schedule_items(self):
        """
        Used to populate cached_earliest_start_time and cached_latest_end_time.
        Called when schedule items are changed.
        """

        self.with_generated_fields().save(update_fields=self.cached_fields_from_schedule_items)

    @classmethod
    def import_program_from_v1(
        cls,
        event: Event,
        queryset: models.QuerySet[Programme] | None = None,
        clear: bool = False,
    ):
        from programme.models.programme import Programme

        if (meta := event.program_v2_event_meta) is None:
            raise ValueError(f"Event {event.slug} does not have program_v2_event_meta")

        if queryset is None:
            queryset = Programme.objects.filter(category__event=event)

        Importer = meta.importer_class
        importer = Importer(event=event)

        importer.import_dimensions(clear=clear, refresh_cached_dimensions=False)
        return importer.import_program(queryset, clear=clear)

    @cached_property
    def meta(self) -> ProgramV2EventMeta:
        if (meta := self.event.program_v2_event_meta) is None:
            raise TypeError(f"Event {self.event.slug} does not have program_v2_event_meta but Programs are present")

        return meta

    @cached_property
    def timezone(self) -> tzinfo:
        return self.event.timezone

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

    @property
    def is_accepting_feedback(self) -> bool:
        return bool(
            self.meta.is_accepting_feedback
            and self.cached_earliest_start_time
            and now() >= self.cached_earliest_start_time
        )
