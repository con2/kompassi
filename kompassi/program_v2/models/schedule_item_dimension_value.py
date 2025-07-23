from __future__ import annotations

import logging

from django.db import models

from kompassi.core.models import Event
from kompassi.dimensions.models.dimension_value import DimensionValue

from .program import Program
from .schedule_item import ScheduleItem

logger = logging.getLogger(__name__)


class ScheduleItemDimensionValue(models.Model):
    id: int

    subject: models.ForeignKey[ScheduleItem] = models.ForeignKey(
        ScheduleItem,
        on_delete=models.CASCADE,
        related_name="dimensions",
    )
    value: models.ForeignKey[DimensionValue] = models.ForeignKey(
        DimensionValue,
        on_delete=models.CASCADE,
        related_name="+",
    )

    def __str__(self):
        return f"{self.value.dimension}={self.value}"

    @property
    def program(self) -> Program:
        return self.subject.program

    @property
    def event(self) -> Event:
        event = self.value.dimension.universe.scope.event

        if event is None:
            raise ValueError(f"Event not found for ScheduleItemDimensionValue {self}")

        return event

    class Meta:
        unique_together = ("subject", "value")

        # NOTE: only implements the `manual` ordering for now
        # See https://con2.slack.com/archives/C3ZGNGY48/p1718446605681339
        ordering = ("value__dimension__order", "value__order")
