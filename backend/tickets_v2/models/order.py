from __future__ import annotations

from decimal import Decimal
from functools import cached_property
from typing import TYPE_CHECKING, Self

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat, Lower
from lippukala.models.order import Order as LippukalaOrder

from core.models.event import Event
from dimensions.graphql.dimension_filter_input import DimensionFilterInput
from event_log_v2.utils.monthly_partitions import UUID7Mixin
from graphql_api.language import SUPPORTED_LANGUAGES

from ..optimized_server.models.enums import PaymentProvider, PaymentStampType, PaymentStatus, RefundType
from ..optimized_server.models.order import OrderProduct
from ..optimized_server.utils.formatting import format_order_number
from ..optimized_server.utils.uuid7 import uuid7
from ..utils.event_partitions import EventPartitionsMixin
from .meta import TicketsV2EventMeta
from .product import Product

if TYPE_CHECKING:
    from .payment_stamp import PaymentStamp
    from .receipt import Receipt


PRODUCT_CACHE: dict[int, dict[int, Product]] = {}


class OrderMixin:
    @cached_property
    def formatted_order_number(self) -> str:
        return format_order_number(self.order_number)  # type: ignore

    @classmethod
    def _get_product(cls, event_id: int, product_id: int):
        """
        Products are immutable once sold, so it's safe to cache them forever (or for the lifetime of the process).
        If a product is changed after a single instance is sold, a new product version is created that supersedes the old one.
        If a super admin mutates a product from taka-admin, they should restart the worker to clear the cache.
        """
        if found := PRODUCT_CACHE.get(event_id, {}).get(product_id):
            return found

        PRODUCT_CACHE[event_id] = {
            p.id: p
            for p in Product.objects.filter(event_id=event_id).only(
                "title",
                "description",
                "price",
                "etickets_per_product",
            )
        }

        return PRODUCT_CACHE[event_id][product_id]

    @cached_property
    def products(self) -> list[OrderProduct]:
        return [
            OrderProduct(
                title=product.title,
                price=product.price,
                quantity=quantity,
            )
            for product_id, quantity in self.product_data.items()  # type: ignore
            if quantity > 0 and (product := self._get_product(self.event_id, product_id))  # type: ignore
        ]

    @cached_property
    def etickets(self) -> list[Product]:
        """
        Returns the Product for each instance of an eticket in the order.
        Each product may specify zero to any number of etickets per product
        (eg. Valentine's Day pair ticket).
        """
        return [
            product
            for product_id, quantity in self.product_data.items()  # type: ignore
            if (product := self._get_product(self.event_id, product_id))  # type: ignore
            for _ in range(product.etickets_per_product)
            for _ in range(quantity)
        ]

    @property
    def have_etickets(self) -> bool:
        return bool(self.etickets)

    @property
    def lippukala_order(self):
        """
        Returns the Lippukala order if it exists, or None.
        Use `get_or_create_lippukala_order` to have it created if it doesn't exist.
        """
        return LippukalaOrder.objects.filter(reference_number=self.formatted_order_number).first()


class Order(OrderMixin, EventPartitionsMixin, UUID7Mixin, models.Model):
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
    phone = models.TextField(blank=True, default="")

    event_id: int

    @cached_property
    def timezone(self):
        return self.event.timezone

    @property
    def tickets(self):
        from .ticket import Ticket

        return Ticket.objects.filter(event=self.event, order_id=self.id)

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

    @cached_property
    def meta(self) -> TicketsV2EventMeta:
        return TicketsV2EventMeta.objects.get(event_id=self.event_id)

    @property
    def scope(self):
        return self.event.scope

    def cancel(self) -> PaymentStamp:
        from .payment_stamp import PaymentStamp

        if self.cached_status >= PaymentStatus.CANCELLED:
            raise ValueError("Order is already cancelled")

        cancelled_stamp = PaymentStamp(
            event=self.event,
            order_id=self.id,
            correlation_id=uuid7(),
            provider_id=PaymentProvider.NONE,
            type=PaymentStampType.CANCEL_WITHOUT_REFUND,
            status=PaymentStatus.CANCELLED,
            data={},
        )
        cancelled_stamp.save()
        return cancelled_stamp

    def refund(self, refund_type: RefundType) -> PaymentStamp:
        from .payment_stamp import PaymentStamp

        if self.cached_status == PaymentStatus.REFUNDED:
            raise ValueError("Order is already refunded")

        paid_stamp = self.payment_stamps.filter(status=PaymentStatus.PAID).order_by("-id").first()
        if not paid_stamp:
            raise ValueError("Cannot refund an order that has not been paid")

        match refund_type:
            case RefundType.MANUAL:
                refund_stamp = PaymentStamp(
                    event=self.event,
                    order_id=self.id,
                    correlation_id=uuid7(),
                    provider_id=PaymentProvider.NONE,
                    type=PaymentStampType.MANUAL_REFUND,
                    status=PaymentStatus.REFUNDED,
                    data={},
                )
            case RefundType.PROVIDER:
                # FIXME Paytrail API usage occurs within transaction
                # Disable ATOMIC_REQUESTS and manage transactions in GraphQL manually
                # 1. Save request stamp, commit
                # 2. Talk to Paytrail outside of transaction
                # 3. Save response stamp, commit
                prepared_refund_request = self.meta.provider.prepare_refund(paid_stamp)
                prepared_refund_request.request_stamp.save()
                _response, refund_stamp = prepared_refund_request.send()
            case _:
                raise ValueError(f"Unsupported refund type: {refund_type}")

        refund_stamp.save()
        return refund_stamp
