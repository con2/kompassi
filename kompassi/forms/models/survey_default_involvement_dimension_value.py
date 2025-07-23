from __future__ import annotations

import logging

from django.db import models

from kompassi.dimensions.models.dimension_value import DimensionValue

from .survey import Survey

logger = logging.getLogger(__name__)


class SurveyDefaultInvolvementDimensionValue(models.Model):
    """
    When an involvement is created based on a response to a survey
    the default dimension values are set on the involvement.
    """

    subject: models.ForeignKey[Survey] = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name="default_involvement_dimensions",
    )
    value: models.ForeignKey[DimensionValue] = models.ForeignKey(
        DimensionValue,
        on_delete=models.CASCADE,
        related_name="+",
    )

    def __str__(self):
        return f"{self.value.dimension}={self.value}"

    class Meta:
        unique_together = ("subject", "value")
