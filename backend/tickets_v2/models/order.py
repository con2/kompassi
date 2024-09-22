from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Literal

from django.contrib.auth.models import User
from django.db import models

from core.models.event import Event
from event_log_v2.utils.monthly_partitions import UUID7Mixin
from event_log_v2.utils.uuid7 import uuid7
from tickets.utils import append_reference_number_checksum

from ..utils.event_partitions import EventPartitionsMixin
from .product import Product

if TYPE_CHECKING:
    pass

OrderState = Literal["unpaid", "paid", "cancelled"]


class Order(EventPartitionsMixin, UUID7Mixin, models.Model):
    """
    Partitioned by event_id.
    Primary key is (event_id, id).
    Migrations managed manually.

    NOTE: We are cheating! The UUIDField called `id` is actually not the primary key of this model.
    Instead, the primary key is a composite key of (event_id, id).
    This is because PostgreSQL requires the partition key to be part of the primary key.
    Django, on the other hand, does not support composite primary keys.

    NOTE: Only create orders via the query in ../optimized_server/models/sql/create_order.sql
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid7,
        editable=False,
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.RESTRICT,
        related_name="+",
    )

    customer_data = models.JSONField(
        default=dict,
        help_text="{firstName, lastName, phone, email}",
    )
    product_data = models.JSONField(
        default=dict,
        help_text="product id -> quantity",
    )

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # NOTE: confirmed_at is called timestamp and backed by id which is UUID7
    paid_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    cached_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal(0),
    )

    event_id: int

    @property
    def tickets(self):
        from .ticket import Ticket

        return Ticket.objects.filter(event=self.event, order_id=self.id)

    @property
    def price_cents(self):
        return int(self.cached_price * 100)

    @property
    def products(self) -> list[tuple[Product, int]]:
        products_by_id = {product.id: product for product in Product.objects.filter(event=self.event)}
        return [
            (products_by_id[product_id], quantity)
            for (product_id, quantity) in self.product_data.items()
            if quantity > 0
        ]

    @property
    def reference_number_base(self):
        return str(self.id.int % 10**19)

    # TODO persist
    @property
    def reference_number(self):
        return append_reference_number_checksum(self.reference_number_base)

    @property
    def formatted_reference_number(self):
        return "".join((i if (n + 1) % 5 else i + " ") for (n, i) in enumerate(self.reference_number[::-1]))[::-1]
