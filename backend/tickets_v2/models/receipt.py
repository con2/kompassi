from __future__ import annotations

import json
from decimal import Decimal
from functools import cached_property
from pathlib import Path
from typing import ClassVar, Self
from urllib.parse import urlparse
from uuid import UUID

import pydantic
from django.conf import settings
from django.core.mail import EmailMessage
from django.db import connection, models
from django.template.loader import render_to_string
from lippukala.models import Code
from lippukala.models import Order as LippukalaOrder
from lippukala.printing import OrderPrinter

from core.models.event import Event
from event_log_v2.utils.monthly_partitions import UUID7Mixin, uuid7
from graphql_api.language import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGE_CODES
from tickets.lippukala_integration import Queue as LippukalaQueue

from ..optimized_server.models.enums import ReceiptStatus, ReceiptType
from ..optimized_server.utils.formatting import format_money, format_order_number
from ..utils.event_partitions import EventPartitionsMixin
from .order import Order
from .product import Product

# TODO missing Swedish (message template too)
ETICKET_TEXT = dict(
    fi="Tässä sähköiset lippusi {event_name} -tapahtumaan. Kiitos tilauksestasi!",
    en="Here are your e-tickets for {event_name}. Thank you for your order!",
)
ETICKET_SUBJECT = dict(
    fi="E-lippu",
    en="E-ticket",
)
RECEIPT_SUBJECT = dict(
    fi="Tilausvahvistus",
    en="Order confirmation",
)

FROM_EMAIL: str = settings.DEFAULT_FROM_EMAIL
KOMPASSI_V2_BASE_URL: str = settings.KOMPASSI_V2_BASE_URL
SHOP_HOSTNAME = urlparse(KOMPASSI_V2_BASE_URL).hostname  # 'v2.kompassi.eu'
MAIL_DOMAIN = FROM_EMAIL.split("@", 1)[1].rstrip(">")
LIPPUKALA_PREFIX = LippukalaQueue.ONE_QUEUE
ETICKET_FILENAME = "e-ticket.pdf"


class Receipt(EventPartitionsMixin, UUID7Mixin, models.Model):
    """
    Receipt stamps are created for paid orders to indicate various stages of
    receipt and electronic ticket delivery. The table is strictly insert only;
    no updates or deletes will ever be made.

    Partitioned by event_id.
    Primary key is (event_id, id).
    Migrations managed manually.
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

    order_id = models.UUIDField(
        null=True,
        blank=True,
    )

    correlation_id = models.UUIDField(
        help_text=(
            "The correlation ID ties together the receipt stamps related to the same receipt attempt. "
            "Usually you would use the correlation ID of the payment stamp that you used to determine this order is paid."
        ),
    )

    batch_id = models.UUIDField(
        null=True,
        blank=True,
        help_text=(
            "The ID of the batch this receipt was sent processed in. "
            "This is an UUIDv7 that is generated when the batch is created. "
            "If the receipt is stuck in PROCESSING and the batch ID is old, then the batch has probably failed and needs to be retried."
        ),
    )

    type = models.SmallIntegerField(
        choices=[(t.value, t.name) for t in ReceiptType],
    )

    status = models.SmallIntegerField(
        choices=[(s.value, s.name) for s in ReceiptStatus],
    )

    email = models.EmailField(
        blank=True,
        default="",
        help_text="The email address to which the receipt was sent.",
    )

    event_id: int
    pk: UUID

    @cached_property
    def order(self):
        """
        Direct the query to the correct partition.
        """
        return Order.objects.get(event=self.event, id=self.order_id)

    @property
    def timezone(self):
        return self.event.timezone


class LocalizedOrderPrinter(OrderPrinter):
    """
    Overrides some texts of the default lippukala.printing.OrderPrinter
    to better support non-Finnish-speaking customers.

    TODO Upstream this
    """

    event_name: str
    event_slug: str

    def __init__(self, language: str, event_name: str, event_slug: str):
        super().__init__(print_logo_path=None)
        self.language = language
        self.event_name = event_name
        self.event_slug = event_slug

    def get_heading_texts(self, order: LippukalaOrder, n_orders: int) -> list[str | None]:
        match self.language:
            case "fi":
                return [
                    (f"Tilausnumero: {order.reference_number}" if order.reference_number else None),
                    f"Tilausaika: {order.created_on.strftime('%d.%m.%Y klo %H:%M')}",
                    f"Kauppa: {KOMPASSI_V2_BASE_URL}/{self.event_slug}/tickets",
                    f"Tapahtuma: {self.event_name}",
                ]
            case _:
                return [
                    (f"Order number: {order.reference_number}" if order.reference_number else None),
                    f"Order time: {order.created_on.strftime('%Y-%m-%d %H:%M')}",
                    f"Shop: {KOMPASSI_V2_BASE_URL}/{self.event_slug}/tickets",
                    f"Event: {self.event_name}",
                ]


class PendingReceipt(pydantic.BaseModel, arbitrary_types_allowed=True, frozen=True):
    """
    Responsible for sending email receipts and generating eticket PDFs.
    Also as such represents an item of work to be done by the receipt worker.
    It results in a receipt being sent to the customer, with or without e-tickets.
    Should contain all the information it needs to do its job (save for easily cacheable stuff).
    """

    receipt_id: UUID = pydantic.Field(default_factory=uuid7)
    order_id: UUID
    event_id: int
    event_name: str
    event_slug: str
    language: str
    first_name: str
    last_name: str
    email: str
    phone: str
    product_data: dict[int, int]
    order_number: int
    total_price: Decimal

    # NOTE: fields and their order must match fields returned by the query
    query: ClassVar[str] = (Path(__file__).parent / "sql" / "claim_pending_receipts.sql").read_text()
    batch_size: ClassVar[int] = 100
    product_cache: ClassVar[dict[int, dict[int, Product]]] = {}

    @pydantic.field_validator("language", mode="before")
    @staticmethod
    def validate_language(value: str):
        if value not in SUPPORTED_LANGUAGE_CODES:
            return DEFAULT_LANGUAGE

        # TODO Missing Swedish message template
        if value == "sv":
            return "en"

        return value

    @pydantic.field_validator("product_data", mode="before")
    @staticmethod
    def validate_product_data(value: str | dict[str, int]):
        if isinstance(value, str):
            return json.loads(value)

        return value

    @pydantic.computed_field
    @cached_property
    def formatted_order_number(self) -> str:
        return format_order_number(self.order_number)

    @pydantic.computed_field
    @cached_property
    def formatted_total_price(self) -> str:
        return format_money(self.total_price)

    @classmethod
    def _get_product(cls, event_id: int, product_id: int):
        """
        Products are immutable once sold, so it's safe to cache them forever (or for the lifetime of the process).
        If a product is changed after a single instance is sold, a new product version is created that supersedes the old one.
        If a super admin mutates a product from taka-admin, they should restart the worker to clear the cache.
        """
        if found := cls.product_cache.get(event_id, {}).get(product_id):
            return found

        cls.product_cache[event_id] = {
            p.id: p
            for p in Product.objects.filter(event_id=event_id).only(
                "title",
                "description",
                "price",
                "etickets_per_product",
            )
        }

        return cls.product_cache[event_id][product_id]

    @pydantic.computed_field
    @cached_property
    def products(self) -> list[tuple[Product, int]]:
        return [
            (
                self._get_product(self.event_id, product_id),
                quantity,
            )
            for product_id, quantity in self.product_data.items()
            if quantity > 0
        ]

    @cached_property
    def etickets(self) -> list[Product]:
        return [
            product
            for product, quantity in self.products
            for _ in range(quantity * product.etickets_per_product)
            if product.etickets_per_product > 0
        ]

    @pydantic.computed_field
    @cached_property
    def have_etickets(self) -> bool:
        return bool(self.etickets)

    def eticket_text(self) -> str:
        return ETICKET_TEXT[self.language].format(event_name=self.event_name)

    @classmethod
    def claim_pending_receipts(cls, event_id: int, batch_size: int = batch_size) -> tuple[list[Self], bool]:
        """
        Iterate this to find orders for which a receipt needs to be sent.
        You'll get a batch of `ReceiptPending.batch_size` orders at a time, and
        a boolean telling if there's more orders to process
        (ie. a subsequent call to this method will return more orders).
        """
        with connection.cursor() as cursor:
            cursor.execute(
                cls.query,
                dict(
                    batch_id=uuid7(),
                    batch_size=batch_size + 1,
                    event_id=event_id,
                ),
            )
            results = [
                cls(**dict(zip(cls.model_fields, row, strict=True)))  # type: ignore
                for row in cursor
            ]

        if have_more := len(results) > batch_size:
            results.pop(batch_size)

        return results, have_more

    @staticmethod
    def make_code(lippukala_order: LippukalaOrder, product: Product) -> Code:
        """
        Generate computed fields as Code.__init__ does to allow bulk_create.
        """
        code = Code(
            order=lippukala_order,
            prefix=LIPPUKALA_PREFIX,
            product_text=product.title,
        )

        code.code = code._generate_code()
        code.literate_code = code._generate_literate_code()

        return code

    def get_lippukala_order(self) -> LippukalaOrder | None:
        if not self.have_etickets:
            return None

        lippukala_order, created = LippukalaOrder.objects.get_or_create(
            # order number makes more sense to customer and event personnel than (bank) reference number
            reference_number=self.formatted_order_number,
            defaults=dict(
                event=self.event_slug,
                address_text=f"{self.first_name} {self.last_name}\n{self.email}",
                free_text=self.eticket_text,
            ),
        )

        if not created:
            return lippukala_order

        Code.objects.bulk_create(
            self.make_code(
                lippukala_order,
                product,
            )
            for product in self.etickets
        )

        return lippukala_order

    def get_etickets_pdf(self) -> bytes | None:
        lippukala_order = self.get_lippukala_order()
        if not lippukala_order:
            return None

        printer = LocalizedOrderPrinter(self.language, self.event_name, self.event_slug)
        printer.process_order(lippukala_order)
        return printer.finish()

    def send_receipt(self, from_email: str = FROM_EMAIL, mail_domain: str = MAIL_DOMAIN):
        if etickets_pdf := self.get_etickets_pdf():
            subject = ETICKET_SUBJECT[self.language]
        else:
            subject = RECEIPT_SUBJECT[self.language]

        body = render_to_string(
            f"tickets_v2_receipt_{self.language}.eml",
            self.model_dump(mode="python", by_alias=False),
        )
        subject = f"{self.event_name}: {subject} ({self.formatted_order_number})"

        # NOTE doesn't check this internal alias exists (perf), too bad if it doesn't
        reply_to_email = (f"{self.event_slug}-tickets@{mail_domain}",)
        to_email = (f"{self.first_name} {self.last_name} <{self.email}>",)

        # uncomment to see the receipts on terminal & write etickets to file
        # if settings.DEBUG:
        #     print(subject, body, sep="\n\n", end="\n\n")
        #     if etickets_pdf:
        #         path = Path("dev-secrets") / f"eticket-{self.order_id}.pdf"
        #         with path.open("wb") as f:
        #             f.write(etickets_pdf)
        #         print("Wrote attachment to", path)

        message = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            reply_to=reply_to_email,
            to=to_email,
        )

        if etickets_pdf:
            message.attach(ETICKET_FILENAME, etickets_pdf, "application/pdf")

        message.send(fail_silently=True)

    @classmethod
    def from_order(cls, order: Order) -> Self:
        return cls(
            order_id=order.id,
            event_id=order.event_id,
            event_name=order.event.name,
            event_slug=order.event.slug,
            language=order.language,
            first_name=order.first_name,
            last_name=order.last_name,
            email=order.email,
            phone=order.phone,
            product_data=order.product_data,
            order_number=order.order_number,
            total_price=order.cached_price,
        )
