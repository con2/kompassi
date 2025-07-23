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
from django.db import connection, models, transaction
from django.template.loader import render_to_string
from lippukala.models import Code
from lippukala.models import Order as LippukalaOrder
from lippukala.printing import OrderPrinter

from kompassi.core.models.event import Event
from kompassi.event_log_v2.utils.monthly_partitions import UUID7Mixin, uuid7, uuid7_to_datetime
from kompassi.graphql_api.language import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGE_CODES
from kompassi.tickets_v2.lippukala_integration import Queue as LippukalaQueue

from ..optimized_server.models.enums import PaymentStatus, ReceiptStatus, ReceiptType
from ..utils.event_partitions import EventPartitionsMixin
from .order import Order, OrderMixin
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
CANCELLED_SUBJECT = dict(
    fi="Tilaus peruutettu",
    en="Order cancelled",
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


EVENT_CACHE: dict[int, Event] = {}


class PendingReceipt(OrderMixin, pydantic.BaseModel, arbitrary_types_allowed=True, frozen=True):
    """
    Responsible for sending email receipts and generating eticket PDFs.
    Also as such represents an item of work to be done by the receipt worker.
    It results in a receipt being sent to the customer, with or without e-tickets.
    Should contain all the information it needs to do its job (save for easily cacheable stuff).
    """

    receipt_id: UUID = pydantic.Field(default_factory=uuid7)
    receipt_type: ReceiptType
    order_id: UUID
    event_id: int
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

    @property
    def order_date(self):
        return uuid7_to_datetime(self.order_id)

    @pydantic.field_validator("language", mode="before")
    @staticmethod
    def validate_language(value: str):
        value = value.lower()

        # TODO Missing Swedish message template
        if value == "sv":
            return "en"

        if value not in SUPPORTED_LANGUAGE_CODES:
            return DEFAULT_LANGUAGE

        return value

    @pydantic.field_validator("product_data", mode="before")
    @staticmethod
    def validate_product_data(value: str | dict[str, int]):
        if isinstance(value, str):
            return json.loads(value)

        return value

    @classmethod
    def _get_event(cls, event_id: int):
        if found := EVENT_CACHE.get(event_id):
            return found

        EVENT_CACHE.update(
            {
                event.id: event
                for event in Event.objects.filter(ticketsv2eventmeta__isnull=False).only(
                    "name",
                    "slug",
                    "timezone_name",
                )
            }
        )

        return EVENT_CACHE[event_id]

    @cached_property
    def event(self) -> Event:
        return self._get_event(self.event_id)

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

    def get_or_create_lippukala_order(self) -> LippukalaOrder | None:
        if not self.have_etickets:
            return None

        eticket_text = ETICKET_TEXT[self.language].format(event_name=self.event.name)

        # There is a rare case where a huge order may receive duplicate ticket codes.
        # In that case, let the IntegrityError rollback this transaction.
        # Then we can (manually) create a new Receipt, which will then retry
        # creating the LippukalaOrder and Codes.
        # Without the transaction, the LippukalaOrder might be created without Codes.
        with transaction.atomic():
            lippukala_order, created = LippukalaOrder.objects.get_or_create(
                reference_number=str(self.order_id),
                defaults=dict(
                    event=self.event.slug,
                    address_text=f"{self.first_name} {self.last_name}\n{self.email}",
                    free_text=eticket_text,
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
        if self.receipt_type != ReceiptType.PAID:
            return None

        lippukala_order = self.get_or_create_lippukala_order()
        if not lippukala_order:
            return None

        printer = LocalizedOrderPrinter(self)
        printer.process_order(lippukala_order)
        return printer.finish()

    @property
    def body(self) -> str:
        match self.receipt_type:
            case ReceiptType.PAID:
                template_name = f"tickets_v2_receipt_{self.language}.eml"
            case ReceiptType.CANCELLED | ReceiptType.REFUNDED:
                template_name = f"tickets_v2_cancel_{self.language}.eml"
            case _:
                raise ValueError("Unknown receipt type")

        vars = dict(
            event_name=self.event.name,
            order_number=self.order_number,
            products=self.products,
            total_price=self.total_price,
            have_etickets=self.have_etickets,
            is_refund=self.receipt_type == ReceiptType.REFUNDED,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
        )
        return render_to_string(template_name, vars)

    @property
    def subject(self) -> str:
        match self.receipt_type:
            case ReceiptType.PAID if self.have_etickets:
                subject = ETICKET_SUBJECT[self.language]
            case ReceiptType.PAID:
                subject = RECEIPT_SUBJECT[self.language]
            case ReceiptType.CANCELLED | ReceiptType.REFUNDED:
                subject = CANCELLED_SUBJECT[self.language]
            case _:
                raise ValueError("Unknown receipt type")

        return f"{self.event.name}: {subject} ({self.formatted_order_number})"

    def send_receipt(self, from_email: str = FROM_EMAIL, mail_domain: str = MAIL_DOMAIN):
        # NOTE doesn't check this internal alias exists (perf), too bad if it doesn't
        reply_to_email = (f"{self.event.slug}-tickets@{mail_domain}",)
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
            subject=self.subject,
            body=self.body,
            from_email=from_email,
            reply_to=reply_to_email,
            to=to_email,
        )

        if etickets_pdf := self.get_etickets_pdf():
            message.attach(ETICKET_FILENAME, etickets_pdf, "application/pdf")

        message.send(fail_silently=True)

    @classmethod
    def from_order(cls, order: Order) -> Self:
        if order.cached_status < PaymentStatus.PAID:
            raise ValueError("No receipt for unpaid orders")

        return cls(
            order_id=order.id,
            receipt_type=PaymentStatus(order.cached_status).to_receipt_type(),
            event_id=order.event_id,
            language=order.language,
            first_name=order.first_name,
            last_name=order.last_name,
            email=order.email,
            phone=order.phone,
            product_data=order.product_data,
            order_number=order.order_number,
            total_price=order.cached_price,
        )


class LocalizedOrderPrinter(OrderPrinter):
    """
    Overrides some texts of the default lippukala.printing.OrderPrinter
    to better support non-Finnish-speaking customers.

    NOTE: Only process one order at a time.
    """

    receipt: PendingReceipt

    def __init__(self, receipt: PendingReceipt):
        super().__init__(print_logo_path=None)
        self.receipt = receipt

    def get_heading_texts(self, order: LippukalaOrder, n_orders: int) -> list[str | None]:
        timestamp = self.receipt.order_date.astimezone(self.receipt.event.timezone)

        match self.receipt.language:
            case "fi":
                return [
                    f"Tilausnumero: {self.receipt.formatted_order_number}",
                    f"Tilausaika: {timestamp.strftime('%d.%m.%Y klo %H:%M')}",
                    f"Sivusto: {KOMPASSI_V2_BASE_URL}",
                    f"Tapahtuma: {self.receipt.event.name}",
                ]
            case _:
                return [
                    f"Order number: {self.receipt.formatted_order_number}",
                    f"Order time: {timestamp.strftime('%Y-%m-%d %H:%M')}",
                    f"Site: {KOMPASSI_V2_BASE_URL}",
                    f"Event: {self.receipt.event.name}",
                ]
