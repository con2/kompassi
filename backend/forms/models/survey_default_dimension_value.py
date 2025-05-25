from __future__ import annotations

import logging

from django.db import models

from dimensions.models.dimension_value import DimensionValue

from .survey import Survey

logger = logging.getLogger("kompassi")


class SurveyDefaultDimensionValue(models.Model):
    """
    When a response is created, the default dimension values are set on the response.
    """

    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name="default_dimensions",
    )
    value = models.ForeignKey(
        DimensionValue,
        on_delete=models.CASCADE,
        related_name="+",
    )

    def __str__(self):
        return f"{self.value.dimension}={self.value}"

    class Meta:
        unique_together = ("survey", "value")
