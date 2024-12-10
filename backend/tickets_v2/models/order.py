from __future__ import annotations

from decimal import Decimal
from functools import cached_property
from pathlib import Path
from typing import ClassVar
from uuid import UUID

from django.contrib.auth.models import User
from django.db import connection, models

from core.models.event import Event
from event_log_v2.utils.monthly_partitions import UUID7Mixin
from graphql_api.language import SUPPORTED_LANGUAGES
from tickets.utils import append_reference_number_checksum

from ..optimized_server.models.enums import PaymentStatus
from ..optimized_server.models.order import OrderProduct
from ..optimized_server.utils.uuid7 import uuid7
from ..utils.event_partitions import EventPartitionsMixin
from .product import Product


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

    language = models.CharField(
        max_length=2,
        choices=[(lang.code, lang.name_django) for lang in SUPPORTED_LANGUAGES],
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
                title=products_by_id[product_id].title,
                price=products_by_id[product_id].price,
                quantity=quantity,
            )
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

    @property
    def status(self) -> PaymentStatus:
        from .payment_stamp import PaymentStamp

        return PaymentStatus(
            PaymentStamp.objects.filter(
                event_id=self.event_id,
                order_id=self.id,
            ).aggregate(models.Max("status"))["status__max"]
        )


class OrderOwner(EventPartitionsMixin, models.Model):
    """
    Indicates the owner of an order.
    All unclaimed orders with a matching email address are claimed when the email address is confirmed.
    Separate table to keep Order insert only and as fast as possible to read.

    Partitioned by event_id.
    Primary key is (event_id, order_id).
    Migrations managed manually.
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="+")
    order_id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    event_id: int
    have_unclaimed_orders_query: ClassVar[str] = (Path(__file__).parent / "sql/have_unclaimed_orders.sql").read_text()
    claim_orders_query: ClassVar[str] = (Path(__file__).parent / "sql/claim_orders.sql").read_text()
    get_user_order_query: ClassVar[str] = (Path(__file__).parent / "sql/get_user_order.sql").read_text()
    get_user_orders_query: ClassVar[str] = (Path(__file__).parent / "sql/get_user_orders.sql").read_text()

    # the mixin will set statistics 10000 on this column
    intrapartition_id_column: ClassVar[str] = "order_id"

    @classmethod
    def have_unclaimed_orders(cls, user: User):
        """
        Returns true if the user has unlinked orders made with the same email address.
        These orders can be linked to the user account by verifying the email address again.
        """
        with connection.cursor() as cursor:
            cursor.execute(cls.have_unclaimed_orders_query, (user.email,))
            return bool(cursor.fetchone())

    @classmethod
    def claim_orders(cls, user: User):
        """
        Called when a user confirms their email address.
        Claims all unclaimed orders with a matching email address.
        """
        with connection.cursor() as cursor:
            cursor.execute(
                cls.claim_orders_query,
                dict(
                    user_id=user.id,  # type: ignore
                    email=user.email,
                ),
            )

    @classmethod
    def get_user_order(cls, event_slug: str, order_id: UUID | str, user_id: int) -> Order:
        """
        Returns an order of the current user.
        Note that unlinked orders made with the same email address are not returned.
        They need to be linked first (ie. their email confirmed again).
        """
        try:
            return Order.objects.raw(
                cls.get_user_order_query,
                dict(
                    event_slug=event_slug,
                    order_id=order_id,
                    user_id=user_id,
                ),
            )[0]
        except IndexError as e:
            raise Order.DoesNotExist() from e

    @classmethod
    def get_user_orders(cls, user_id: int) -> models.RawQuerySet[Order]:
        """
        Returns the orders of the current user.
        Note that unlinked orders made with the same email address are not returned.
        They need to be linked first (ie. their email confirmed again).
        """
        return Order.objects.raw(
            cls.get_user_orders_query,
            dict(
                user_id=user_id,
            ),
        )
