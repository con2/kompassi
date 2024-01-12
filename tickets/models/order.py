import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, date
from datetime import time as dtime
from pkg_resources import resource_string
from typing import TYPE_CHECKING

from django.db import models, connection
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _

from dateutil.tz import tzlocal

from core.models.event import Event
from core.utils import url

from ..utils import format_date, format_price, append_reference_number_checksum
from .consts import LANGUAGE_CHOICES, UNPAID_CANCEL_HOURS
from .tickets_event_meta import TicketsEventMeta

if TYPE_CHECKING:
    from .order_product import OrderProduct


logger = logging.getLogger("kompassi")


@dataclass
class ArrivalsRow:
    hour: datetime | None
    arrivals: int
    cum_arrivals: int

    QUERY = resource_string(__name__, "queries/arrivals_by_hour.sql").decode()


class Order(models.Model):
    order_product_set: models.QuerySet["OrderProduct"]

    event = models.ForeignKey("core.Event", on_delete=models.CASCADE)

    customer = models.OneToOneField("tickets.Customer", on_delete=models.CASCADE, null=True, blank=True)
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
        default=LANGUAGE_CHOICES[0][0],
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
    def is_overdue(self):
        return self.due_date and self.is_confirmed and not self.is_paid and self.due_date < timezone.now()

    @property
    def is_cancelled(self):
        return self.cancellation_time is not None

    @property
    def price_cents(self):
        # TODO Port to Django DB reduction functions if possible
        return sum(op.price_cents for op in self.order_product_set.all())

    @property
    def requires_accommodation_information(self):
        return self.order_product_set.filter(count__gt=0, product__requires_accommodation_information=True).exists()

    @property
    def formatted_price(self):
        return format_price(self.price_cents)

    @property
    def readable_state(self):
        if self.is_paid:
            return "Paid"
        elif self.is_confirmed:
            if self.is_overdue:
                return f"Confirmed; payment overdue since {self.formatted_due_date}"
            else:
                return f"Confirmed; payment due {self.formatted_due_date}"
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
        assert self.customer is not None
        assert not self.is_confirmed

        self.clean_up_order_products()

        self.reference_number = self._make_reference_number()
        self.confirm_time = timezone.now()
        self.save()

    def confirm_payment(self, payment_date=None, send_email=True):
        assert self.is_confirmed and not self.is_paid

        if payment_date is None:
            payment_date = date.today()

        self.payment_date = payment_date

        self.save()

        if "lippukala" in settings.INSTALLED_APPS:
            self.lippukala_create_codes()

        if send_email:
            self.send_confirmation_message("payment_confirmation")

    def cancel(self, send_email=True):
        assert self.is_confirmed

        if "lippukala" in settings.INSTALLED_APPS:
            self.lippukala_revoke_codes()

        self.cancellation_time = timezone.now()
        self.save()

        if send_email:
            self.send_confirmation_message("cancellation_notice")

    def uncancel(self, send_email=True):
        assert self.is_cancelled

        if "lippukala" in settings.INSTALLED_APPS:
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
    def due_date(self):
        if self.confirm_time:
            return datetime.combine(
                (self.confirm_time + timedelta(days=self.meta.due_days)).date(), dtime(23, 59, 59)
            ).replace(tzinfo=tzlocal())
        else:
            return None

    @property
    def formatted_due_date(self):
        return format_date(self.due_date)

    def checkout_return_url(self, request):
        return request.build_absolute_uri(url("payments_process_view", self.event.slug))

    @property
    def reservation_valid_until(self):
        return (
            self.confirm_time + timedelta(seconds=self.event.tickets_event_meta.reservation_seconds)
            if self.confirm_time
            else None
        )

    @property
    def contains_electronic_tickets(self):
        return self.order_product_set.filter(count__gt=0, product__electronic_ticket=True).exists()

    @property
    def etickets_delivered(self):
        return self.contains_electronic_tickets and self.is_paid

    @property
    def lippukala_prefix(self):
        if "lippukala" not in settings.INSTALLED_APPS:
            raise NotImplementedError("lippukala is not installed")

        from tickets.lippukala_integration import select_queue

        return select_queue(self)

    @property
    def css_class(self):
        if self.is_cancelled:
            return "danger"
        elif self.is_overdue:
            return "warning"
        else:
            return ""

    def lippukala_create_codes(self):
        if "lippukala" not in settings.INSTALLED_APPS:
            raise NotImplementedError("lippukala is not installed")

        if not self.contains_electronic_tickets:
            return

        from lippukala.models import Code, Order as LippukalaOrder

        assert self.customer

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
            for _ in range(op.count * op.product.electronic_tickets_per_product):
                Code.objects.create(
                    order=lippukala_order,
                    prefix=self.lippukala_prefix,
                    product_text=op.product.electronic_ticket_title,
                )

    def lippukala_revoke_codes(self):
        if "lippukala" not in settings.INSTALLED_APPS:
            raise NotImplementedError("lippukala is not installed")

        if not self.lippukala_order:
            return

        from lippukala.consts import UNUSED, MANUAL_INTERVENTION_REQUIRED

        self.lippukala_order.code_set.filter(status=UNUSED).update(status=MANUAL_INTERVENTION_REQUIRED)  # type: ignore

    def lippukala_reinstate_codes(self):
        if "lippukala" not in settings.INSTALLED_APPS:
            raise NotImplementedError("lippukala is not installed")

        if not self.lippukala_order:
            return

        from lippukala.consts import UNUSED, MANUAL_INTERVENTION_REQUIRED

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
        if "lippukala" not in settings.INSTALLED_APPS:
            raise NotImplementedError("lippukala not installed")

        from lippukala.printing import OrderPrinter

        meta = self.event.tickets_event_meta

        printer = OrderPrinter(
            print_logo_path=meta.print_logo_path,
            print_logo_size_cm=meta.print_logo_size_cm,
        )
        printer.process_order(self.lippukala_order)

        return printer.finish()

    def send_confirmation_message(self, msgtype):
        if "background_tasks" in settings.INSTALLED_APPS:
            from ..tasks import order_send_confirmation_message

            order_send_confirmation_message.delay(self.pk, msgtype)  # type: ignore
        else:
            self._send_confirmation_message(msgtype)

    def _send_confirmation_message(self, msgtype: str):
        assert self.customer

        # don't fail silently, warn admins instead
        bcc: list[str] = []
        meta = self.event.tickets_event_meta

        if meta.ticket_spam_email:
            bcc.append(meta.ticket_spam_email)

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
        from .customer import Customer

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
            results = [ArrivalsRow(*row) for row in cursor.fetchall()]

        # TODO backfill missing hours

        return results
