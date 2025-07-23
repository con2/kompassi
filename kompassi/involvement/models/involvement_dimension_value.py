from __future__ import annotations

import logging

from django.db import models

from kompassi.dimensions.models.dimension_value import DimensionValue

from .involvement import Involvement

logger = logging.getLogger(__name__)


class InvolvementDimensionValue(models.Model):
    subject = models.ForeignKey(
        Involvement,
        on_delete=models.CASCADE,
        related_name="dimensions",
    )
    value = models.ForeignKey(
        DimensionValue,
        on_delete=models.CASCADE,
        related_name="+",
    )

    def __str__(self):
        return f"{self.value.dimension}={self.value}" if self.value else "-"

    class Meta:
        unique_together = ("subject", "value")
