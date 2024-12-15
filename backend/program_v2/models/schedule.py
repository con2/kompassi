from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Self

from django.conf import settings
from django.db import models

from core.utils.model_utils import make_slug_field, slugify
from graphql_api.language import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGE_CODES
from graphql_api.utils import getattr_message_in_language

from .program import Program

if TYPE_CHECKING:
    from .dimension_values import ScheduleItemDimensionValue


class ScheduleItem(models.Model):
    id: int

    slug = make_slug_field(
        unique=False,
        help_text=("NOTE: Slug must be unique within Event. It does not suffice to be unique within Program."),
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="schedule_items",
    )

    # NOTE SUPPORTED_LANGUAGES
    subtitle_en = models.TextField()
    subtitle_fi = models.TextField()
    subtitle_sv = models.TextField()

    start_time = models.DateTimeField()
    length = models.DurationField()
    annotations = models.JSONField(
        blank=True,
        default=dict,
        help_text="Own annotations of this schedule item only.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # denormalized fields
    cached_end_time = models.DateTimeField()
    cached_event = models.ForeignKey(
        "core.Event",
        on_delete=models.CASCADE,
        related_name="schedule_items",
    )
    cached_location = models.JSONField(blank=True, default=dict)
    cached_annotations = models.JSONField(
        blank=True,
        default=dict,
        help_text="Combined annotations of this schedule item and its parent program item.",
    )

    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="favorite_schedule_items", blank=True)

    dimensions: models.QuerySet[ScheduleItemDimensionValue]

    class Meta:
        ordering = ["cached_event", "start_time"]
        unique_together = [("cached_event", "slug")]

    def __str__(self):
        return self.get_title()

    def get_title(self, language: str = DEFAULT_LANGUAGE) -> str:
        program_title = getattr_message_in_language(self.program, "title", language)
        schedule_item_subtitle = getattr_message_in_language(self, "subtitle", language)

        if schedule_item_subtitle:
            return f"{program_title} – {schedule_item_subtitle}"
        else:
            return program_title

    @property
    def meta(self):
        return self.program.meta

    @cached_property
    def timezone(self):
        return self.cached_event.timezone

    def _make_slug(self):
        if subtitle := getattr_message_in_language(self, "subtitle", DEFAULT_LANGUAGE):
            return f"{self.program.slug}-{slugify(subtitle)}"
        else:
            return self.program.slug

    batch_size = 100
    cached_fields = [
        "cached_end_time",
        "cached_event",
        "cached_annotations",
        "cached_location",
        "updated_at",
    ]

    def refresh_cached_fields(self):
        self.with_generated_fields().save(update_fields=self.cached_fields)

    @classmethod
    def refresh_cached_fields_qs(cls, queryset: models.QuerySet[Self]):
        cls.objects.bulk_update(
            [sitem.with_generated_fields() for sitem in queryset],
            fields=cls.cached_fields,
            batch_size=cls.batch_size,
        )

    def _build_dimensions(self):
        dimensions = {k: list(vs) for (k, vs) in self.program.cached_dimensions.values()}
        for sidv in self.dimensions.all():
            dimensions.setdefault(sidv.value.dimension.slug, []).append(sidv.value.slug)
        return dimensions

    def _build_location(self):
        localized_locations: dict[str, set[str]] = {}

        if location_dimension := self.meta.location_dimension:
            for pdv in self.dimensions.filter(value__dimension=location_dimension).distinct():
                for language_code in SUPPORTED_LANGUAGE_CODES:
                    title = getattr_message_in_language(pdv.value, "title", language_code)
                    localized_locations.setdefault(language_code, set()).add(title)

        # if both "foo" and "foo, bar" are present, only "foo, bar" is included
        for locations in localized_locations.values():
            for location in list(locations):
                for other_location in list(locations):
                    if location != other_location and location in other_location and location in locations:
                        locations.remove(location)

        return {lang: ", ".join(locations) for lang, locations in localized_locations.items() if locations}

    def with_generated_fields(self) -> Self:
        if self.program is None:
            raise ValueError("Program is required to generate fields for ScheduleItem")

        if not self.slug:
            self.slug = self._make_slug()

        self.cached_event = self.program.event
        self.cached_dimensions = self._build_dimensions()
        self.cached_location = self._build_location()
        self.cached_annotations = {**self.program.annotations, **self.annotations}

        if self.start_time is not None and self.length is not None:
            self.cached_end_time = self.start_time + self.length

        return self
