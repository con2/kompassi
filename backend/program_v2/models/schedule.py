from __future__ import annotations

from typing import TYPE_CHECKING, Self

from django.db import models

from core.utils.model_utils import make_slug_field, slugify

from .program import Program

if TYPE_CHECKING:
    pass


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
    subtitle = models.CharField(max_length=255, blank=True)
    start_time = models.DateTimeField()
    length = models.DurationField()

    # denormalized fields
    cached_end_time = models.DateTimeField()
    cached_event = models.ForeignKey(
        "core.Event",
        on_delete=models.CASCADE,
        related_name="schedule_items",
    )
    cached_location = models.JSONField(blank=True, default=dict)

    class Meta:
        ordering = ["cached_event", "start_time"]
        unique_together = [("cached_event", "slug")]

    def __str__(self):
        return self.title

    @property
    def title(self):
        if self.subtitle:
            return f"{self.program.title} – {self.subtitle}"
        else:
            return self.program.title

    def _make_slug(self):
        if self.subtitle:
            return f"{self.program.slug}-{slugify(self.subtitle)}"
        else:
            return self.program.slug

    def refresh_cached_fields(self, commit=True):
        if self.program:
            self.cached_location = self.program.cached_location
            self.cached_event = self.program.event

        if self.start_time is not None and self.length is not None:
            self.cached_end_time = self.start_time + self.length

        if commit:
            self.save(update_fields=["cached_end_time", "cached_event", "cached_location"])

    def with_generated_fields(self) -> Self:
        """
        Use this when creating "floating" ScheduleItems for eg. bulk creation.
        """
        if self.program and not self.slug:
            self.slug = self._make_slug()

        self.refresh_cached_fields(commit=False)

        return self
