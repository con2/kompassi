from __future__ import annotations

from decimal import Decimal
from functools import cached_property
from typing import TYPE_CHECKING, Self

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat, Lower

from core.models.event import Event
from dimensions.graphql.dimension_filter_input import DimensionFilterInput
from event_log_v2.utils.monthly_partitions import UUID7Mixin
from graphql_api.language import SUPPORTED_LANGUAGES

from ..optimized_server.models.enums import PaymentStatus
from ..optimized_server.models.order import OrderProduct
from ..optimized_server.utils.uuid7 import uuid7
from ..utils.event_partitions import EventPartitionsMixin
from .product import Product

if TYPE_CHECKING:
    from .payment_stamp import PaymentStamp
    from .receipt import Receipt


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

    order_number = models.IntegerField(
        help_text=(
            "Order number used in contexts where UUID cannot be used. "
            "Such places include generating reference numbers and "
            "the customer reading the order number aloud to an event rep. "
            "Prefer id (UUID) for everything else (eg. URLs)."
        )
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    cached_status = models.SmallIntegerField(
        choices=[(status.value, status.name) for status in PaymentStatus],
        default=PaymentStatus.NOT_STARTED,
        help_text="Payment status of the order. Updated by a trigger on PaymentStamp.",
    )

    cached_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal(0),
        help_text="Total price of the order in euros. Calculated by create_order.sql from product_data.",
    )

    language = models.CharField(
        max_length=2,
        choices=[(lang.code, lang.name_django) for lang in SUPPORTED_LANGUAGES],
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

    @cached_property
    def timezone(self):
        return self.event.timezone

    @property
    def tickets(self):
        from .ticket import Ticket

        return Ticket.objects.filter(event=self.event, order_id=self.id)

    @property
    def price_cents(self):
        return int(self.cached_price * 100)

    @cached_property
    def products(self) -> list[OrderProduct]:
        products_by_id = {product.id: product for product in Product.objects.filter(event=self.event)}
        return [
            OrderProduct(
                title=product.title,
                price=product.price,
                quantity=quantity,
            )
            for (product_id, quantity) in self.product_data.items()
            if (product := products_by_id[int(product_id)]) and quantity > 0
        ]

    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def filter_orders(
        cls,
        orders: models.QuerySet[Self],
        filters: list[DimensionFilterInput] | None = None,
        search: str = "",
    ) -> models.QuerySet[Self]:
        if filters:
            for filter in filters:
                values = filter.values
                match filter.dimension:
                    case "status":
                        # resolve status name -> int value
                        values = [PaymentStatus[value.upper()].value for value in values]
                        orders = orders.filter(cached_status__in=values)
                    case "product":
                        orders = orders.filter(product_data__has_keys=values)

        if search:
            # in case search is a formatted order number
            search = search.lstrip("#").lstrip("0")

            # none of these fields is allowed to be null, so coalesce is not needed
            orders = orders.annotate(
                search=Lower(
                    Concat(
                        "first_name",
                        Value(" "),
                        "last_name",
                        Value(" "),
                        "email",
                        Value(" "),
                        "order_number",
                        output_field=models.TextField(),
                    )
                ),
            ).filter(search__contains=search.lower())

        return orders

    @property
    def payment_stamps(self) -> models.QuerySet[PaymentStamp]:
        from .payment_stamp import PaymentStamp

        return PaymentStamp.objects.filter(
            event_id=self.event_id,
            order_id=self.id,
        )

    @property
    def receipts(self) -> models.QuerySet[Receipt]:
        from .receipt import Receipt

        return Receipt.objects.filter(
            event_id=self.event_id,
            order_id=self.id,
        )
