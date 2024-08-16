from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from .program import Program

if TYPE_CHECKING:
    pass


class ScheduleItem(models.Model):
    id: int

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="schedule_items")
    subtitle = models.CharField(max_length=255, blank=True)
    start_time = models.DateTimeField()
    length = models.DurationField()

    # denormalized fields
    cached_end_time = models.DateTimeField()
    cached_location = models.JSONField(blank=True, default=dict)

    def __str__(self):
        return self.title

    @property
    def title(self):
        if self.subtitle:
            return f"{self.program.title} – {self.subtitle}"
        else:
            return self.program.title

    def refresh_cached_fields(self):
        """
        NOTE: cached_location is refreshed from Program.refresh_cached_dimensions
        """
        self.cached_end_time = self.start_time + self.length
        self.save(update_fields=["cached_end_time"])
