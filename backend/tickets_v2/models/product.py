from __future__ import annotations

from pathlib import Path
from typing import ClassVar

import pydantic
from django.db import connection, models
from django.http import HttpRequest
from django.utils.timezone import now

from access.cbac import is_graphql_allowed_for_model
from core.models.event import Event

from .quota import Quota


class ProductCounters(pydantic.BaseModel):
    count_paid: int
    count_reserved: int = pydantic.Field(
        description=(
            "Total number of active reservations for this product including paid and unpaid orders, "
            "excluding cancelled orders."
        ),
    )
    count_ever_reserved: int = pydantic.Field(
        description="Total number of reservations ever made for this product including cancelled orders.",
    )

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

        with connection.cursor() as cursor:
            cursor.execute(ProductCounters.amounts_sold_query, dict(event_id=event_id))
            result = {
                product_id: ProductCounters(
                    count_paid=count_paid,
                    count_reserved=count_reserved,
                    count_ever_reserved=count_ever_reserved,
                )
                for product_id, count_paid, count_reserved, count_ever_reserved in cursor
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

    ordering = models.PositiveSmallIntegerField(default=0)
    max_per_order = models.PositiveSmallIntegerField(default=5)
    etickets_per_product = models.PositiveSmallIntegerField(default=1)

    superseded_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
    )

    available_from = models.DateTimeField(null=True, blank=True)
    available_until = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.TextField()
    description = models.TextField()

    quotas = models.ManyToManyField(
        Quota,
        related_name="products",
    )

    # TODO make into a field to allow for zero or multiple e-tickets per product
    # NOTE grep for it when you do
    event_id: int
    superseded_by_id: int | None

    def __str__(self):
        return f"{self.title} ({self.event})"

    @property
    def is_available(self) -> bool:
        t = now()
        return (
            self.superseded_by is None
            and self.available_from is not None
            and t >= self.available_from
            and (self.available_until is None or t < self.available_until)
        )

    @property
    def timezone(self):
        return self.event.timezone

    @property
    def scope(self):
        return self.event.scope

    def get_counters(self, request: HttpRequest | None) -> ProductCounters:
        effective_product_id = self.superseded_by_id or self.id
        return ProductCounters.get_for_event(self.event_id, request)[effective_product_id]

    def can_be_deleted_by(self, request: HttpRequest) -> bool:
        return self.get_counters(request).count_ever_reserved == 0 and is_graphql_allowed_for_model(
            request.user,
            instance=self,
            operation="delete",
            field="self",
        )
