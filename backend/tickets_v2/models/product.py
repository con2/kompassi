from __future__ import annotations

from typing import Literal

from django.db import models

from core.models.event import Event

from ..optimized_server.utils.formatting import format_money
from .quota import Quota


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

    # TODO make into a field to allow for zero or multiple e-tickets per product
    # NOTE grep for it when you do
    electronic_tickets_per_product: Literal[1] = 1
    event_id: int

    @property
    def price_cents(self) -> int:
        return int(self.price * 100)

    @property
    def formatted_price(self) -> str:
        return format_money(self.price)
