from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Literal

import pydantic
from django.db import connection, models
from django.http import HttpRequest
from django.utils.timezone import now

from core.models.event import Event

from .quota import Quota


class ProductCounters(pydantic.BaseModel):
    count_paid: int
    count_reserved: int
    # count_available: int

    amounts_sold_query: ClassVar[str] = (Path(__file__).parent / "sql" / "get_product_counters.sql").read_text()

    @staticmethod
    def get_for_event(event_id: int, request: HttpRequest | None) -> dict[int, ProductCounters]:
        """
        Returns dict of product_id -> amount_sold for the event.
        Return amounts of sold products for each product in the event.
        Old versions of products are grouped under the current version.
        Cached per request.
        """
        # event_id -> product_id -> ProductCounters
        cache: dict[int, dict[int, ProductCounters]] | None = getattr(request, "_tickets_v2_product_counters", None)
        if cache is None:
            cache = {}
            if request is not None:
                request._tickets_v2_product_counters = cache  # type: ignore

        if event_cache := cache.get(event_id):
            return event_cache

        # quota_counters = QuotaCounters.get_for_event(event_id, request)

        with connection.cursor() as cursor:
            cursor.execute(ProductCounters.amounts_sold_query, dict(event_id=event_id))
            result = {
                product_id: ProductCounters(
                    count_paid=count_paid,
                    count_reserved=count_reserved,
                    # count_available=min(quota_counters[quota_id].count_available for quota_id in quotas),
                )
                for product_id, count_paid, count_reserved in cursor
            }

        cache[event_id] = result
        return result


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
    superseded_by_id: int | None

    @property
    def price_cents(self) -> int:
        return int(self.price * 100)

    @property
    def is_available(self) -> bool:
        t = now()
        return (
            self.superseded_by is None
            and self.available_from is not None
            and t >= self.available_from
            and (self.available_until is None or t < self.available_until)
        )

    def get_counters(self, request: HttpRequest | None) -> ProductCounters:
        return ProductCounters.get_for_event(self.event_id, request)[self.id]
