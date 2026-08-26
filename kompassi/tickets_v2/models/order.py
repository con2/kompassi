from __future__ import annotations

import logging
from datetime import datetime, timedelta
from decimal import Decimal
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Self

from django.conf import settings
from django.contrib.auth.models import User
from django.db import connection, models, transaction
from django.db.models import Value
from django.db.models.functions import Concat, Lower
from django.http import HttpRequest
from django.urls import reverse
from django.utils.timezone import get_current_timezone
from django.utils.timezone import now as django_now
from lippukala.models.code import Code as LippukalaCode
from lippukala.models.order import Order as LippukalaOrder

from kompassi.access.cbac import is_graphql_allowed_for_model
from kompassi.core.models.event import Event
from kompassi.dimensions.graphql.dimension_filter_input import DimensionFilterInput
from kompassi.event_log_v2.utils.emit import emit
from kompassi.event_log_v2.utils.monthly_partitions import UUID7Mixin
from kompassi.graphql_api.language import SUPPORTED_LANGUAGES

from ..optimized_server.models.enums import PaymentProvider, PaymentStampType, PaymentStatus, RefundType
from ..optimized_server.models.order import OrderProduct, VatBreakdownLine
from ..optimized_server.utils.cancellation import (
    get_cancellation_deadline,
    get_payment_deadline,
    is_cancellable_by_customer,
)
from ..optimized_server.utils.formatting import format_order_number
from ..optimized_server.utils.uuid7 import uuid7
from ..utils.event_partitions import EventPartitionsMixin
from .enums import ActorType
from .fields import PostgresEnumField
from .meta import TicketsV2EventMeta
from .product import Product

if TYPE_CHECKING:
    from .payment_stamp import PaymentStamp
    from .receipt import Receipt


PRODUCT_CACHE: dict[int, dict[int, Product]] = {}
logger = logging.getLogger(__name__)


class OrderStateChanged(Exception):
    """
    Raised by Order.fulfil() and Order.cancel_and_refund() when the caller's
    fromPaymentStatus no longer matches the order's actual status under
    select_for_update — ie. another admin, or an automatic process, already
    acted on the order since the caller last read its state.
    """

    def __init__(self, actual_status: PaymentStatus):
        self.actual_status = actual_status
        super().__init__(f"Order is no longer in the expected status (actual status: {actual_status.name})")


class OrderMixin:
    """
    Common functionality used by Order and PendingReceipt.
    """

    @cached_property
    def formatted_order_number(self) -> str:
        return format_order_number(self.order_number)  # type: ignore

    @classmethod
    def _get_product(cls, event_id: int | str, product_id: int | str) -> Product:
        """
        Products are immutable once sold, so it's safe to cache them forever (or for the lifetime of the process).
        If a product is changed after a single instance is sold, a new product version is created that supersedes the old one.
        If a super admin mutates a product from taka-admin, they should restart the worker to clear the cache.
        """
        event_id = int(event_id)
        product_id = int(product_id)

        if found := PRODUCT_CACHE.get(event_id, {}).get(product_id):
            return found

        PRODUCT_CACHE[event_id] = {
            p.id: p
            for p in Product.objects.filter(event_id=event_id).only(
                "title",
                "description",
                "price",
                "vat_percentage",
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
                vat_percentage=product.vat_percentage,
            )
            for product_id, quantity in self.product_data.items()  # type: ignore
            if quantity > 0 and (product := self._get_product(self.event_id, product_id))  # type: ignore
        ]

    @cached_property
    def vat_breakdown(self) -> list[VatBreakdownLine]:
        return VatBreakdownLine.from_order_products(self.products)

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

    cached_status = PostgresEnumField(
        enum=PaymentStatus,
        db_type_name="tickets_v2_paymentstatus",
        choices=[(status.name, status.name) for status in PaymentStatus],
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

    @property
    def status(self) -> PaymentStatus:
        return self.cached_status

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
                vat_percentage=product.vat_percentage,
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
                        product_ids = [int(value) for value in values]
                        old_versions_by_current: dict[int, list[int]] = {}
                        for old_id, current_id in Product.objects.filter(superseded_by_id__in=product_ids).values_list(
                            "id", "superseded_by_id"
                        ):
                            old_versions_by_current.setdefault(current_id, []).append(old_id)

                        query = models.Q()
                        for product_id in product_ids:
                            keys = [
                                str(product_id),
                                *(str(old_id) for old_id in old_versions_by_current.get(product_id, [])),
                            ]
                            sub_query = models.Q()
                            for key in keys:
                                sub_query |= models.Q(product_data__has_key=key)
                            query &= sub_query
                        orders = orders.filter(query)

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
        ).order_by("id")

    @property
    def receipts(self) -> models.QuerySet[Receipt]:
        from .receipt import Receipt

        return Receipt.objects.filter(
            event_id=self.event_id,
            order_id=self.id,
        ).order_by("id")

    @cached_property
    def meta(self) -> TicketsV2EventMeta:
        return TicketsV2EventMeta.objects.get(event_id=self.event_id)

    @property
    def scope(self):
        return self.event.scope

    @property
    def lippukala_order(self):
        """
        Returns the Lippukala order if it exists, or None.
        Use `get_or_create_lippukala_order` to have it created if it doesn't exist.
        """
        return LippukalaOrder.objects.filter(
            reference_number=str(self.id),  # type: ignore
        ).first()

    @property
    def lippukala_codes(self):
        return (
            LippukalaCode.objects.filter(order=lippukala_order)
            if (lippukala_order := self.lippukala_order)
            else LippukalaCode.objects.none()
        )

    @property
    def admin_url(self):
        return f"{settings.KOMPASSI_V2_BASE_URL}/{self.event.slug}/orders-admin/{self.id}"

    def get_etickets_link(self, request: HttpRequest):
        if self.cached_status != PaymentStatus.PAID:
            return None

        if not self.have_etickets:
            return None

        return request.build_absolute_uri(
            reverse(
                "tickets_v2:etickets_view",
                kwargs=dict(
                    event_slug=self.event.slug,
                    order_id=self.id,
                ),
            )
        )

    def can_be_cancelled_by_owner(self, user: User):
        return (
            self.status.is_owner_cancelable and self.owner is not None and user.is_authenticated and user == self.owner
        )

    @property
    def provider_paid_stamps(self) -> models.QuerySet[PaymentStamp]:
        """
        PAID stamps recorded by an actual payment provider (as opposed to eg.
        an admin marking the order as paid). Only these can be provider refunded.
        """
        return self.payment_stamps.filter(status=PaymentStatus.PAID).exclude(provider=PaymentProvider.NONE)

    @property
    def cancellation_deadline(self) -> datetime | None:
        return get_cancellation_deadline(
            order_created_at=self.timestamp,
            cancellation_period_days=self.meta.cancellation_period_days,
            event_start_time=self.event.start_time,
        )

    @property
    def payment_deadline(self) -> datetime | None:
        return get_payment_deadline(
            order_created_at=self.timestamp,
            unpaid_order_cancellation_delay_minutes=self.meta.unpaid_order_cancellation_delay_minutes,
        )

    def can_be_cancelled_by_customer(self) -> bool:
        return is_cancellable_by_customer(
            status=self.status,
            cancellation_deadline=self.cancellation_deadline,
            now=django_now(),
            total_price=self.cached_price,
            is_paid_by_provider=self.provider_paid_stamps.exists,
        )

    def can_be_provider_refunded_by(self, request: HttpRequest):
        # TODO should this method do all the same checks that cancel_and_refund does?
        return (
            self.status.is_refundable
            and self.cached_price > 0
            and self.provider_paid_stamps.exists()
            and is_graphql_allowed_for_model(
                request.user,
                instance=self,
                operation="update",
                field="self",
            )
        )

    def can_be_manually_refunded_by(self, request: HttpRequest):
        return (
            self.status.is_refundable
            and self.payment_stamps.filter(status=PaymentStatus.PAID).exists()
            and is_graphql_allowed_for_model(
                request.user,
                instance=self,
                operation="update",
                field="self",
            )
        )

    def can_be_paid_by(self, _request: HttpRequest | None = None):
        return self.status.is_payable and self.cached_price > 0

    @staticmethod
    def _build_internal_payment_stamp_data(
        actor_type: ActorType = ActorType.ADMIN,
        actor_user: User | None = None,
    ):
        return dict(
            __actorType=actor_type.value,
            __actorUserId=actor_user.id if actor_user else None,  # type: ignore
        )

    def emit_event_log_entry(
        self,
        entry_type: str,
        *,
        actor_type: ActorType = ActorType.ADMIN,
        actor_user: User | None = None,
    ):
        return emit(
            entry_type,
            event=self.event,
            order=self.id,
            order_number=self.formatted_order_number,
            actor_type=actor_type,
            actor=actor_user,
            context=self.admin_url,
        )

    def cancel_and_refund(
        self,
        refund_type: RefundType,
        *,
        from_status: PaymentStatus | None = None,
        actor_type: ActorType = ActorType.ADMIN,
        actor_user: User | None = None,
    ):
        """
        from_status, when given, is checked against the order's status under
        select_for_update, raising OrderStateChanged on mismatch. Pass it
        whenever the caller's belief about the order's status can be stale by
        the time this runs (eg. an admin page left open) — the automatic
        cancellation sweep has no such stale belief and omits it.
        """
        from lippukala.consts import MANUAL_INTERVENTION_REQUIRED, UNUSED

        from .payment_stamp import PaymentStamp

        data = self._build_internal_payment_stamp_data(
            actor_type=actor_type,
            actor_user=actor_user,
        )

        with transaction.atomic():
            order = self
            if from_status is not None:
                order = Order.objects.select_for_update().get(event=self.event, id=self.id)
                if order.cached_status != from_status:
                    raise OrderStateChanged(order.cached_status)

            match refund_type:
                case RefundType.NONE:
                    if order.cached_status == PaymentStatus.CANCELLED:
                        raise ValueError("Order is already cancelled")

                    prepared_request = None
                    request_stamp = PaymentStamp(
                        event=order.event,
                        order_id=order.id,
                        correlation_id=uuid7(),
                        provider=PaymentProvider.NONE,
                        type=PaymentStampType.CANCEL_WITHOUT_REFUND,
                        status=PaymentStatus.CANCELLED,
                        data=data,
                    )

                case RefundType.MANUAL:
                    if order.cached_status == PaymentStatus.REFUNDED:
                        raise ValueError("Order is already refunded")

                    prepared_request = None
                    request_stamp = PaymentStamp(
                        event=order.event,
                        order_id=order.id,
                        correlation_id=uuid7(),
                        provider=PaymentProvider.NONE,
                        type=PaymentStampType.MANUAL_REFUND,
                        status=PaymentStatus.REFUNDED,
                        data=data,
                    )
                case RefundType.PROVIDER:
                    if order.cached_status == PaymentStatus.REFUNDED:
                        raise ValueError("Order is already refunded")

                    # NOTE: must be a provider stamp — the order may additionally have been
                    # marked as paid by an admin, recording a PAID stamp with provider NONE
                    # that cannot be refunded via the provider.
                    paid_stamp = order.provider_paid_stamps.order_by("-id").first()
                    if not paid_stamp:
                        raise ValueError("Cannot refund an order that has not been paid via a payment provider")

                    prepared_request = order.meta.provider_implementation.prepare_refund(paid_stamp)
                    request_stamp = prepared_request.request_stamp
                    request_stamp.data = dict(request_stamp.data or {}, **data)
                case _:
                    raise ValueError(f"Unsupported refund type: {refund_type}")

            request_stamp.save()

            # Release tickets consumed from quotas
            order.tickets.update(order_id=None)

            # Invalidate electronic tickets
            if lippukala_order := order.lippukala_order:
                LippukalaCode.objects.filter(
                    order=lippukala_order,
                    status=UNUSED,
                ).update(
                    status=MANUAL_INTERVENTION_REQUIRED,
                )

            order.emit_event_log_entry(
                refund_type.event_log_entry_type,
                actor_type=actor_type,
                actor_user=actor_user,
            )

        response_stamp = None
        if prepared_request:
            _response, response_stamp = prepared_request.send()

        if response_stamp:
            with transaction.atomic():
                response_stamp.save()

    @classmethod
    def cancel_unpaid_orders(
        cls,
        now: datetime | None = None,
        actor_type: ActorType = ActorType.SYSTEM,
        actor_user: User | None = None,
    ):
        """
        Cancels unpaid orders older than each event's configured cancellation
        window (TicketsV2EventMeta.unpaid_order_cancellation_delay_minutes).

        0 (the default) keeps the legacy rule: unpaid orders done before
        midnight three days ago are cancelled, which in practice gives an
        order a multi-day grace period since this only runs once a day. A
        configured delay in minutes replaces that with a precise, much
        shorter window, and is expected to run from a frequent cron.
        """
        tz = get_current_timezone()
        if now is None:
            now = datetime.now(tz)

        for meta in TicketsV2EventMeta.objects.all():
            if meta.unpaid_order_cancellation_delay_minutes:
                threshold = now - timedelta(minutes=meta.unpaid_order_cancellation_delay_minutes)
            else:
                threshold = (now - timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0)

            orders = cls.objects.filter(
                event_id=meta.event_id,
                cached_status__lt=PaymentStatus.PAID,
                id__lt=uuid7(threshold),
            )

            if num_orders := orders.count():
                logger.info(
                    "Cancelling %d unpaid orders older than %s in event %s",
                    num_orders,
                    threshold,
                    meta.event_id,
                )
                for order in orders:
                    order.cancel_and_refund(
                        refund_type=RefundType.NONE,
                        actor_type=actor_type,
                        actor_user=actor_user,
                    )
            else:
                logger.info(
                    "No unpaid orders older than %s to cancel in event %s",
                    threshold,
                    meta.event_id,
                )

    def can_be_fulfilled_by(self, request: HttpRequest):
        return self.status.is_fulfillable and is_graphql_allowed_for_model(
            request.user,
            instance=self,
            operation="update",
            field="self",
        )

    _ensure_tickets_query: ClassVar[str] = "select tickets_v2_ensure_tickets(%s, %s)"
    _ticket_shortfall_query: ClassVar[str] = (
        Path(__file__).parent / "sql" / "get_order_ticket_shortfall.sql"
    ).read_text()

    def _ensure_tickets(self) -> bool:
        """
        Idempotently claims from the free pool whatever this order is short of.
        Returns whether the order now holds its full expected complement.
        """
        with connection.cursor() as cursor:
            cursor.execute(self._ensure_tickets_query, [self.event_id, self.id])
            (result,) = cursor.fetchone()
        return result

    def _get_ticket_shortfall(self) -> dict[int, int]:
        """
        Returns quota id -> number of tickets this order is short of.
        """
        with connection.cursor() as cursor:
            cursor.execute(self._ticket_shortfall_query, dict(event_id=self.event_id, order_id=self.id))
            return dict(cursor.fetchall())

    def fulfil(
        self,
        from_status: PaymentStatus,
        actor_type: ActorType = ActorType.ADMIN,
        actor_user: User | None = None,
    ):
        """
        Ensures the order holds its expected tickets, minting into the quota
        whatever the free pool cannot cover, then records it as paid.

        For an order that already holds its tickets (NOT_STARTED, PENDING,
        FAILED — ie. today's "mark as paid") the minting step is a no-op. For
        a PAID_AFTER_CANCELLATION order this is the admin's "make it so":
        overselling the quota by exactly the amount owed, deliberately.
        """
        from .payment_stamp import PaymentStamp
        from .quota import Quota

        with transaction.atomic():
            order = Order.objects.select_for_update().get(event=self.event, id=self.id)
            if order.cached_status != from_status:
                raise OrderStateChanged(order.cached_status)

            order._ensure_tickets()
            for quota_id, quantity in order._get_ticket_shortfall().items():
                Quota.objects.get(id=quota_id).create_tickets(quantity)
            order._ensure_tickets()

            data = self._build_internal_payment_stamp_data(
                actor_type=actor_type,
                actor_user=actor_user,
            )
            PaymentStamp(
                event=order.event,
                order_id=order.id,
                correlation_id=uuid7(),
                provider=PaymentProvider.NONE,
                type=PaymentStampType.MANUAL_FULFILMENT,
                status=PaymentStatus.PAID,
                data=data,
            ).save()

            order.emit_event_log_entry(
                "tickets_v2.order.fulfilled",
                actor_type=actor_type,
                actor_user=actor_user,
            )

    @classmethod
    def retry_paid_after_cancellation(cls):
        """
        Attempts to fulfil, for free, every order flagged PAID_AFTER_CANCELLATION —
        this becomes possible as soon as other unpaid orders are cancelled and
        release their tickets. Unlike Order.fulfil(), this never grows a quota:
        overselling is a decision reserved for a human, never one a cron takes.
        Checking before stamping also keeps the insert-only PaymentStamp table
        from accumulating a dead stamp per order on every run that finds nothing
        to do.
        """
        from .payment_stamp import PaymentStamp

        for order in cls.objects.filter(cached_status=PaymentStatus.PAID_AFTER_CANCELLATION):
            with transaction.atomic():
                locked_order = cls.objects.select_for_update().get(event=order.event, id=order.id)
                if locked_order.cached_status != PaymentStatus.PAID_AFTER_CANCELLATION:
                    continue

                if locked_order._ensure_tickets():
                    data = cls._build_internal_payment_stamp_data(actor_type=ActorType.SYSTEM)
                    PaymentStamp(
                        event=locked_order.event,
                        order_id=locked_order.id,
                        correlation_id=uuid7(),
                        provider=PaymentProvider.NONE,
                        type=PaymentStampType.PAYMENT_CALLBACK,
                        status=PaymentStatus.PAID,
                        data=data,
                    ).save()
                else:
                    # Resolve everything the log line needs before set_rollback(True),
                    # since Django refuses further queries once it is called.
                    formatted_order_number = locked_order.formatted_order_number
                    admin_url = locked_order.admin_url

                    # tickets_v2_ensure_tickets() already rolled back its own claim
                    # attempt; nothing to undo here beyond releasing the row lock.
                    transaction.set_rollback(True)
                    logger.warning(
                        "Order %s remains flagged as paid after cancellation: %s",
                        formatted_order_number,
                        admin_url,
                    )
