from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import TYPE_CHECKING

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import connection, models
from django.template.loader import render_to_string
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _

from kompassi.core.models.event import Event
from kompassi.core.utils.cleanup import register_cleanup
from kompassi.core.utils.pkg_resources_compat import resource_string
from kompassi.graphql_api.language import DEFAULT_LANGUAGE, get_language_choices

from ..utils import append_reference_number_checksum, format_price
from .LEGACY_TICKETSV1_consts import UNPAID_CANCEL_HOURS
from .LEGACY_TICKETSV1_customer import Customer
from .LEGACY_TICKETSV1_tickets_event_meta import TicketsEventMeta

if TYPE_CHECKING:
    from .LEGACY_TICKETSV1_order_product import OrderProduct


logger = logging.getLogger(__name__)


@dataclass
class ArrivalsRow:
    hour: datetime | None
    arrivals: int
    cum_arrivals: int

    QUERY = resource_string(__name__, "queries/arrivals_by_hour.sql").decode()


@register_cleanup(
    # Unconfirmed orders for past events (with a safety margin of 30 days)
    lambda qs: qs.filter(
        event__start_time__lt=timezone.now() - timedelta(days=30),
        confirm_time__isnull=True,
    )
)
class Order(models.Model):
    order_product_set: models.QuerySet[OrderProduct]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)

    confirm_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Tilausaika",
    )

    ip_address = models.CharField(max_length=15, null=True, blank=True, verbose_name="Tilaajan IP-osoite")

    payment_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Maksupäivä",
    )

    cancellation_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Peruutusaika",
    )

    reference_number = models.CharField(
        max_length=31,
        blank=True,
        verbose_name="Viitenumero",
        db_index=True,
    )

    language = models.CharField(
        max_length=2,
        blank=True,
        choices=get_language_choices(),
        default=DEFAULT_LANGUAGE,
        verbose_name="Kieli",
    )

    @property
    def is_active(self):
        return self.is_confirmed and not self.is_cancelled

    @property
    def is_confirmed(self):
        return self.confirm_time is not None

    @property
    def is_paid(self):
        return self.payment_date is not None

    @property
    def is_cancelled(self):
        return self.cancellation_time is not None

    @property
    def price_cents(self):
        return self.order_product_set.aggregate(
            sum=models.Sum(models.F("product__price_cents") * models.F("count")),
        )["sum"]

    @property
    def formatted_price(self):
        return format_price(self.price_cents)

    @property
    def readable_state(self):
        if self.is_cancelled:
            return "Cancelled"
        elif self.is_paid:
            return "Paid"
        elif self.is_confirmed:
            return "Confirmed"
        else:
            return "Unconfirmed"

    @property
    def reference_number_base(self):
        return self.event.tickets_event_meta.reference_number_template.format(self.pk)

    def _make_reference_number(self):
        return append_reference_number_checksum(self.reference_number_base)

    @property
    def formatted_reference_number(self):
        return "".join((i if (n + 1) % 5 else i + " ") for (n, i) in enumerate(self.reference_number[::-1]))[::-1]

    @property
    def formatted_order_number(self):
        return f"#{self.pk:06d}"

    @property
    def formatted_order_products(self):
        return ", ".join(f"{op.count}x {op.product.name}" for op in self.nonzero_order_products)

    @property
    def nonzero_order_products(self):
        return self.order_product_set.filter(count__gt=0)

    def clean_up_order_products(self):
        self.order_product_set.filter(count__lte=0).delete()

    def confirm_order(self):
        if not self.customer:
            raise ValueError("Customer not set")
        if self.is_confirmed:
            raise ValueError("Already confirmed")

        self.clean_up_order_products()

        self.reference_number = self._make_reference_number()
        self.confirm_time = timezone.now()
        self.save()

    def confirm_payment(self, payment_date=None, send_email=True):
        if not self.is_confirmed:
            raise ValueError("Must be confirmed to pay")
        if self.is_paid:
            raise ValueError("Already paid")

        if payment_date is None:
            payment_date = date.today()

        self.payment_date = payment_date

        self.save()

        self.lippukala_create_codes()

        if send_email:
            self.send_confirmation_message("payment_confirmation")

    def cancel(self, send_email=True):
        if not self.is_confirmed:
            raise ValueError("Must be confirmed to cancel")

        self.lippukala_revoke_codes()

        self.cancellation_time = timezone.now()
        self.save()

        if send_email:
            self.send_confirmation_message("cancellation_notice")

    def uncancel(self, send_email=True):
        if not self.is_cancelled:
            raise ValueError("Must be cancelled to uncancel")

        self.lippukala_reinstate_codes()

        self.cancellation_time = None
        self.save()

        if send_email:
            self.send_confirmation_message("uncancellation_notice")

    @property
    def meta(self):
        return self.event.tickets_event_meta

    @property
    def messages(self):
        return {
            op.product.mail_description
            for op in self.order_product_set.all()
            if op.product.mail_description and op.count > 0
        }

    @property
    def email_vars(self):
        return dict(order=self)

    @property
    def contains_electronic_tickets(self):
        return self.order_product_set.filter(count__gt=0, product__electronic_ticket=True).exists()

    @property
    def etickets_delivered(self):
        return self.contains_electronic_tickets and self.is_paid

    @property
    def lippukala_prefix(self):
        from kompassi.tickets_v2.lippukala_integration import select_queue

        return select_queue(self)

    @property
    def css_class(self):
        if self.is_cancelled:
            return "danger"
        else:
            return ""

    def lippukala_create_codes(self):
        if not self.contains_electronic_tickets:
            return

        from lippukala.models import Code
        from lippukala.models import Order as LippukalaOrder

        if not self.customer:
            raise ValueError("Customer must be set")

        lippukala_order, created = LippukalaOrder.objects.get_or_create(
            reference_number=self.reference_number,
            defaults=dict(
                event=self.event.slug,
                address_text=self.customer.name,
                free_text=self.event.tickets_event_meta.ticket_free_text,
            ),
        )

        if not created:
            logger.debug("Lippukala order already exists")
            return

        for op in self.order_product_set.filter(count__gt=0, product__electronic_ticket=True):
            for _i in range(op.count * op.product.electronic_tickets_per_product):
                Code.objects.create(
                    order=lippukala_order,
                    prefix=self.lippukala_prefix,
                    product_text=op.product.electronic_ticket_title,
                )

    def lippukala_revoke_codes(self):
        if not self.lippukala_order:
            return

        from lippukala.consts import MANUAL_INTERVENTION_REQUIRED, UNUSED

        self.lippukala_order.code_set.filter(status=UNUSED).update(status=MANUAL_INTERVENTION_REQUIRED)  # type: ignore

    def lippukala_reinstate_codes(self):
        if not self.lippukala_order:
            return

        from lippukala.consts import MANUAL_INTERVENTION_REQUIRED, UNUSED

        self.lippukala_order.code_set.filter(status=MANUAL_INTERVENTION_REQUIRED).update(status=UNUSED)  # type: ignore

    @classmethod
    def lippukala_get_order(cls, lippukala_order):
        return cls.objects.get(reference_number=lippukala_order.reference_number)

    @property
    def lippukala_order(self):
        from lippukala.models import Order as LippukalaOrder

        try:
            return LippukalaOrder.objects.get(reference_number=self.reference_number)
        except LippukalaOrder.DoesNotExist:
            return None

    def get_etickets_pdf(self):
        from lippukala.printing import OrderPrinter

        meta = self.event.tickets_event_meta

        printer = OrderPrinter(
            print_logo_path=meta.print_logo_path,
            print_logo_size_cm=meta.print_logo_size_cm,
        )
        printer.process_order(self.lippukala_order)

        return printer.finish()

    def send_confirmation_message(self, msgtype):
        # from ..tasks import order_send_confirmation_message

        # order_send_confirmation_message.delay(self.pk, msgtype)  # type: ignore
        pass

    def _send_confirmation_message(self, msgtype: str):
        if not self.customer:
            raise ValueError("Customer must be set")

        # don't fail silently, warn admins instead
        bcc: list[str] = []

        for op in self.order_product_set.filter(count__gt=0):
            if op.product.notify_email:
                bcc.append(op.product.notify_email)

        attachments: list[tuple[str, bytes, str]] = []  # filename, content, mimetype
        language = self.language if self.language in ["fi", "en"] else "fi"

        if msgtype == "payment_confirmation":
            if self.contains_electronic_tickets:
                attachments.append(("e-lippu.pdf", self.get_etickets_pdf(), "application/pdf"))
                msgsubject = _("E-ticket")
                msgbody = render_to_string(f"email/{language}/tickets_confirm_payment.eml", self.email_vars)
            else:
                msgsubject = _("Order confirmation")
                msgbody = render_to_string(f"email/{language}/tickets_confirm_payment.eml", self.email_vars)
        elif msgtype == "cancellation_notice":
            msgsubject = _("Order cancelled")
            msgbody = render_to_string(f"email/{language}/tickets_cancellation_notice.eml", self.email_vars)
        elif msgtype == "uncancellation_notice":
            msgsubject = _("Order reinstated")
            msgbody = render_to_string(f"email/{language}/tickets_uncancellation_notice.eml", self.email_vars)
        else:
            raise NotImplementedError(msgtype)

        with translation.override(self.language):
            msgsubject = f"{self.event.name}: {msgsubject} ({self.formatted_order_number})"

        if settings.DEBUG:
            print(msgsubject)
            print("=" * len(msgsubject))
            print()
            print(msgbody)
            print()

        message = EmailMessage(
            subject=msgsubject,
            body=msgbody,
            from_email=self.event.tickets_event_meta.cloaked_contact_email,
            to=(self.customer.name_and_email,),
            bcc=bcc,
        )

        for attachment in attachments:
            message.attach(*attachment)

        message.send(fail_silently=True)

    def __str__(self):
        if self.pk:
            return f"#{self.pk} {self.formatted_price} ({self.readable_state})"
        else:
            return "<unsaved order>"

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    @classmethod
    def get_or_create_dummy(cls, event=None):
        from .LEGACY_TICKETSV1_customer import Customer

        if event is None:
            meta, unused = TicketsEventMeta.get_or_create_dummy()
            event = meta.event

        customer, unused = Customer.get_or_create_dummy()

        return cls.objects.get_or_create(
            event=event,
            customer=customer,
        )

    @classmethod
    def get_unpaid_orders_to_cancel(cls, event, hours=UNPAID_CANCEL_HOURS):
        deadline = timezone.now() - timedelta(hours=hours)
        return cls.objects.filter(
            event=event,
            confirm_time__lte=deadline,
            payment_date__isnull=True,
            cancellation_time__isnull=True,
        )

    @classmethod
    def cancel_unpaid_orders(cls, event, hours=UNPAID_CANCEL_HOURS, send_email=False):
        orders = cls.get_unpaid_orders_to_cancel(event=event, hours=hours)
        count = orders.count()

        for order in orders:
            order.cancel(send_email=send_email)

        return count

    @staticmethod
    def get_arrivals_by_hour(event: Event | str):
        event_slug = event if isinstance(event, str) else event.slug

        with connection.cursor() as cursor:
            cursor.execute(ArrivalsRow.QUERY, [event_slug])
            return [ArrivalsRow(*row) for row in cursor.fetchall()]
