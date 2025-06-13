from __future__ import annotations

import logging

from django.db import models

from dimensions.models.dimension_value import DimensionValue

from .response import Response

logger = logging.getLogger("kompassi")


class ResponseDimensionValue(models.Model):
    subject: models.ForeignKey[Response] = models.ForeignKey(
        Response,
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

    class Meta:
        unique_together = ("subject", "value")
