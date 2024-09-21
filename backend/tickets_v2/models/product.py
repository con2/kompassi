from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from core.models.event import Event

from .quota import Quota

if TYPE_CHECKING:
    pass


class Product(models.Model):
    id: int

    event = models.ForeignKey(
        Event,
        on_delete=models.RESTRICT,
        related_name="products",
    )

    title = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    superseded_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
    )

    # NOTE: Must both be set to be available
    available_from = models.DateTimeField(null=True, blank=True)
    available_until = models.DateTimeField(null=True, blank=True)

    quotas = models.ManyToManyField(
        Quota,
        related_name="products",
    )

    event_id: int

    @property
    def price_cents(self) -> int:
        return int(self.price * 100)
