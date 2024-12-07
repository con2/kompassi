from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import models

from core.models.event import Event
from event_log_v2.utils.monthly_partitions import UUID7Mixin
from tickets.utils import append_reference_number_checksum
from tickets_v2.optimized_server.utils.uuid7 import uuid7

from ..utils.event_partitions import EventPartitionsMixin
from .product import Product

if TYPE_CHECKING:
    pass


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

    cached_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal(0),
    )

    order_number = models.IntegerField(
        help_text=(
            "Order number used in contexts where UUID cannot be used. "
            "Such places include generating reference numbers and "
            "the customer reading the order number aloud to an event rep. "
            "Prefer id (UUID) for everything else (eg. URLs)."
        )
    )

    product_data = models.JSONField(
        default=dict,
        help_text="product id -> quantity",
    )

    # NOTE: lengths validated in server code, see optimized_server/models/customer.py
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    phone = models.TextField()

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
