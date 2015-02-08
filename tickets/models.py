# encoding: utf-8

from datetime import datetime, timedelta, date
from datetime import time as dtime
from time import time, mktime

from django.db import models, IntegrityError
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone

from core.models import EventMetaBase
from core.utils import url, code_property
from payments.utils import compute_payment_request_mac

from .utils import format_date, format_price
from .receipt import render_receipt


__all__ = [
    "TicketsEventMeta",
    "Batch",
    "Product",
    "Customer",
    "Order",
    "OrderProduct",
]


LOW_AVAILABILITY_THRESHOLD = 10
UNPAID_CANCEL_DAYS = 1


class TicketsEventMeta(EventMetaBase):
    shipping_and_handling_cents = models.IntegerField(
        verbose_name=u'Toimituskulut (senttejä)',
        default=0,
    )

    due_days = models.IntegerField(
        verbose_name=u'Maksuaika (päiviä)',
        default=14,
    )

    ticket_sales_starts = models.DateTimeField(
        verbose_name=u'Lipunmyynnin alkuaika',
        null=True,
        blank=True,
    )

    ticket_sales_ends = models.DateTimeField(
        verbose_name=u'Lipunmyynnin päättymisaika',
        null=True,
        blank=True,
    )

    reference_number_template = models.CharField(
        max_length=31,
        default="{:04d}",
        verbose_name=u'Viitenumeron formaatti',
        help_text=u'Paikkamerkin {} kohdalle sijoitetaan tilauksen numero. Nollilla täyttäminen esim. {:04d} (4 merkin leveydeltä).',
    )

    contact_email = models.CharField(
        max_length=255,
        verbose_name=u"Asiakaspalvelun sähköpostiosoite selitteineen",
        help_text=u"Ongelmatilanteissa käyttäjää kehotetaan ottamaan yhteyttä tähän osoitteeseen. Muoto: Tracon 9 -lipunmyynti &lt;liput@tracon.fi&gt;",
        blank=True,
    )

    plain_contact_email = models.CharField(
        max_length=255,
        verbose_name=u"Asiakaspalvelun sähköpostiosoite ilman selitettä",
        help_text=u"Ongelmatilanteissa käyttäjää kehotetaan ottamaan yhteyttä tähän osoitteeseen. Muoto: liput@tracon.fi",
        blank=True,
    )

    ticket_spam_email = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=u'Tarkkailusähköposti',
        help_text=u'Kaikki järjestelmän lähettämät sähköpostiviestit lähetetään myös tähän osoitteeseen.',
    )

    reservation_seconds = models.IntegerField(
        verbose_name=u'Varausaika (sekuntia)',
        help_text=u'Käyttäjällä on tämän verran aikaa siirtyä maksamaan ja maksaa tilauksensa tai tilaus perutaan.',
        default=1800,
    )

    ticket_free_text = models.TextField(
        blank=True,
        verbose_name=u'E-lipun teksti',
        help_text=u'Tämä teksti tulostetaan E-lippuun.',
    )

    front_page_text = models.TextField(
        blank=True,
        default=u'',
        verbose_name=u'Etusivun teksti',
        help_text=u'Tämä teksti näytetään lippukaupan ensimmäisellä vaiheella.',
    )

    print_logo_path = models.CharField(
        max_length=255,
        blank=True,
        default=u'',
        verbose_name=u'Logon polku',
        help_text=u'Tämä logo printataan e-lippuun.',
    )

    print_logo_width_mm = models.IntegerField(
        default=0,
        verbose_name=u'Logon leveys (mm)',
        help_text=u'E-lippuun printattavan logon leveys millimetreinä. Suositellaan noin 40 millimetriä leveää logoa.',
    )

    print_logo_height_mm = models.IntegerField(
        default=0,
        verbose_name=u'Logon korkeus (mm)',
        help_text=u'E-lippuun printattavan logon korkeus millimetreinä. Suositellaan noin 20 millimetriä korkeaa logoa.',
    )


    @property
    def print_logo_size_cm(self):
        return (self.print_logo_width_mm / 10.0, self.print_logo_height_mm / 10.0)

    @property
    def is_ticket_sales_open(self):
        t = timezone.now()

        # Starting date must be set for the ticket sales to be considered open
        if not self.ticket_sales_starts:
            return False

        # Starting date must be in the past for the ticket sales to be considered open
        elif self.ticket_sales_starts > t:
            return False

        # If there is an ending date, it must not have been passed yet
        elif self.ticket_sales_ends:
            return t <= self.ticket_sales_ends

        else:
            return True

    @classmethod
    def get_or_create_dummy(cls):
        from django.contrib.auth.models import Group
        from core.models import Event

        group, unused = Group.objects.get_or_create(name='Dummy ticket admin group')
        event, unused = Event.get_or_create_dummy()
        return cls.objects.get_or_create(event=event, defaults=dict(admin_group=group))

    class Meta:
        verbose_name = u'tapahtuman lipunmyyntiasetukset'
        verbose_name_plural = u'tapahtuman lipunmyyntiasetukset'


class Batch(models.Model):
    event = models.ForeignKey('core.Event')

    create_time = models.DateTimeField(auto_now=True)
    delivery_time = models.DateTimeField(null=True, blank=True)

    @property
    def is_delivered(self):
        return self.delivery_time is not None

    @property
    def delivery_date(self):
        return self.delivery_time.date()

    @property
    def readable_state(self):
        if self.is_delivered:
            return u"Delivered at %s" % format_date(self.delivery_time)
        else:
            return u"Awaiting delivery"

    @classmethod
    def create(cls, event, max_items=100):
        # XXX concurrency disaster waiting to happen
        # solution: only I do the botching^Wbatching

        batch = cls(event=event)
        batch.save()

        orders = event.order_set.filter(
            # Order is confirmed
            confirm_time__isnull=False,

            # Order is paid
            payment_date__isnull=False,

            # Order has not yet been allocated into a Batch
            batch__isnull=True,

            # Order has not been cancelled
            cancellation_time__isnull=True
        ).order_by("confirm_time")

        accepted = 0

        for order in orders:
            # TODO do this in the database
            # Some orders need not be shipped.
            if not order.requires_shipping:
                continue

            order.batch = batch
            order.save()

            accepted += 1
            if accepted >= max_items:
                break

        return batch

    def render(self, c):
        for order in self.order_set.all():
            order.render(c)

    @property
    def can_cancel(self):
        return not self.is_delivered

    def cancel(self):
        for order in self.order_set.all():
            order.batch = None
            order.save()

        self.delete()

    @property
    def can_confirm(self):
        return not self.is_delivered

    def confirm(self, delivery_time=None):
        if delivery_time is None:
            delivery_time = timezone.now()

        self.delivery_time = delivery_time
        self.save()
        self.send_delivery_confirmation_messages()

    def send_delivery_confirmation_messages(self):
        if 'background_tasks' in settings.INSTALLED_APPS:
            from .tasks import batch_send_delivery_confirmation_messages
            batch_send_delivery_confirmation_messages.delay(self.pk)
        else:
            self._send_delivery_confirmation_messages()

    def _send_delivery_confirmation_messages(self):
        for order in self.order_set.all():
            order.send_confirmation_message("delivery_confirmation")

    def __unicode__(self):
        return u"#%d (%s)" % (
            self.pk,
            self.readable_state
        )

    class Meta:
        verbose_name = u'toimituserä'
        verbose_name_plural = u'toimituserät'


class LimitGroup(models.Model):
    # REVERSE: product_set = ManyToMany(Product)

    event = models.ForeignKey('core.Event', verbose_name=u'Tapahtuma')
    description = models.CharField(max_length=255, verbose_name=u'Kuvaus')
    limit = models.IntegerField(verbose_name=u'Enimmäismäärä')

    def __unicode__(self):
        return u"{self.description} ({self.amount_available}/{self.limit}".format(self=self)

    class Meta:
        verbose_name = u'loppuunmyyntiryhmä'
        verbose_name_plural = u'loppuunmyyntiryhmät'

    @property
    def amount_sold(self):
        amount_sold = OrderProduct.objects.filter(
            product__limit_groups=self,
            order__confirm_time__isnull=False,
            order__cancellation_time__isnull=True
        ).aggregate(models.Sum('count'))['count__sum']

        return amount_sold if amount_sold is not None else 0

    @property
    def amount_available(self):
        return self.limit - self.amount_sold

    @property
    def is_sold_out(self):
        return self.amount_available < 1

    @property
    def is_availability_low(self):
        return self.amount_available < LOW_AVAILABILITY_THRESHOLD

    @property
    def css_class(self):
        if self.is_sold_out:
            return "danger"
        elif self.is_availability_low:
            return "warning"
        else:
            return ""

    @classmethod
    def get_or_create_dummies(cls):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()

        limit_saturday, unused = cls.objects.get_or_create(event=event, description='Testing saturday', defaults=dict(limit=5000))
        limit_sunday, unused = cls.objects.get_or_create(event=event, description='Testing sunday', defaults=dict(limit=5000))

        return [limit_saturday, limit_sunday]


class Product(models.Model):
    event = models.ForeignKey('core.Event')

    name = models.CharField(max_length=100)
    internal_description = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    mail_description = models.TextField(null=True, blank=True)
    limit_groups = models.ManyToManyField(LimitGroup, blank=True)
    price_cents = models.IntegerField()
    requires_shipping = models.BooleanField(default=True)
    electronic_ticket = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    notify_email = models.CharField(max_length=100, null=True, blank=True)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ('ordering', 'id')

    @property
    def sell_limit(self):
        from warnings import warn
        warn(DeprecationWarning('sell_limit is deprecated, convert everything to use LimitGroup and amount_available directly'))
        return self.amount_available

    @property
    def formatted_price(self):
        return format_price(self.price_cents)

    @property
    def in_stock(self):
        return (self.amount_available > 0)

    @property
    def availability_low(self):
        return (self.amount_available < LOW_AVAILABILITY_THRESHOLD)

    @property
    def amount_available(self):
        return min(group.amount_available for group in self.limit_groups.all())

    @property
    def amount_sold(self):
        cnt = OrderProduct.objects.filter(
            product=self,
            order__confirm_time__isnull=False,
            order__cancellation_time__isnull=True
        ).aggregate(models.Sum('count'))

        sm = cnt['count__sum']
        return sm if sm is not None else 0

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.formatted_price)

    class Meta:
        verbose_name = u'tuote'
        verbose_name_plural = u'tuotteet'

    @classmethod
    def get_or_create_dummy(cls, name='Dummy product', limit_groups=[]):
        meta, unused = TicketsEventMeta.get_or_create_dummy()

        dummy, created = cls.objects.get_or_create(
            event=meta.event,
            name=name,
            defaults=dict(
                description=u'Dummy product for testing',
                price_cents=1800,
                requires_shipping=True,
                available=True,
                ordering=100,
                electronic_ticket=True
            )
        )

        dummy.limit_groups = limit_groups
        dummy.save()

        return dummy, created

    @classmethod
    def get_or_create_dummies(cls):
        [limit_saturday, limit_sunday] = LimitGroup.get_or_create_dummies()

        weekend, unused = cls.get_or_create_dummy('Weekend test product', [limit_saturday, limit_sunday])
        saturday, unused = cls.get_or_create_dummy('Saturday test product', [limit_saturday])
        sunday, unused = cls.get_or_create_dummy('Sunday test product', [limit_sunday])

        return [weekend, saturday, sunday]


# TODO mayhaps combine with Person someday soon?
class Customer(models.Model):
    # REVERSE: order = OneToOne(Order)

    first_name = models.CharField(max_length=100, verbose_name="Etunimi")
    last_name = models.CharField(max_length=100, verbose_name="Sukunimi")
    address = models.CharField(max_length=200, verbose_name="Katuosoite")
    zip_code = models.CharField(max_length=5, verbose_name="Postinumero")
    city = models.CharField(max_length=30, verbose_name="Postitoimipaikka")

    email = models.EmailField(
        verbose_name=u"Sähköpostiosoite",
        help_text=u'Tarkista sähköpostiosoite huolellisesti. Tilausvahvistus sekä mahdolliset sähköiset liput '
            u'lähetetään tähän sähköpostiosoitteeseen. HUOM! Hotmail-osoitteiden kanssa on välillä ollut '
            u'viestien perillemeno-ongelmia. Suosittelemme käyttämään jotain muuta sähköpostiosoitetta kuin Hotmailia.',
    )

    allow_marketing_email = models.BooleanField(
        default=True,
        blank=True,
        verbose_name=u"Minulle saa lähettää tapahtumaan liittyviä tiedotteita sähköpostitse",
    )

    phone_number = models.CharField(max_length=30, null=True, blank=True, verbose_name="Puhelinnumero")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'asiakas'
        verbose_name_plural = u'asiakkaat'

    @property
    def name(self):
        return u"%s %s" % (self.first_name, self.last_name)

    @property
    def sanitized_name(self):
        return u"".join(i for i in self.name if i.isalpha() or i in
            (u'ä', u'Ä', u'ö', u'Ö', u'å', u'Å', u'-', u"'", u" "))

    @property
    def name_and_email(self):
        return u"%s <%s>" % (self.sanitized_name, self.email)

    @classmethod
    def get_or_create_dummy(cls):
        return cls.objects.get_or_create(
            first_name=u'Dummy',
            last_name=u'Testinen',
            defaults=dict(
                email=u'dummy@example.com',
                address=u'Testikuja 5 A 19',
                zip_code=u'12354',
                city=u'Testilä',
            )
        )


class Order(models.Model):
    # REVERSE: order_product_set = ForeignKeyFrom(OrderProduct)

    event = models.ForeignKey('core.Event')

    customer = models.OneToOneField(Customer, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)

    confirm_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Tilausaika',
    )

    ip_address = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name=u'Tilaajan IP-osoite'
    )

    payment_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=u'Maksupäivä',
    )

    cancellation_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Peruutusaika',
    )

    batch = models.ForeignKey(Batch,
        null=True,
        blank=True,
        verbose_name=u'Toimituserä',
    )

    reference_number = models.CharField(
        max_length=31,
        blank=True,
        verbose_name=u'Viitenumero',
    )

    @property
    def is_active(self):
        return self.is_confirmed and not self.is_cancelled

    @property
    def is_outstanding(self):
        return self.is_confirmed and self.requires_shipping and not self.is_cancelled

    @property
    def is_confirmed(self):
        return self.confirm_time is not None

    @property
    def is_paid(self):
        return self.payment_date is not None

    @property
    def is_batched(self):
        return self.batch is not None

    @property
    def is_delivered(self):
        return self.is_batched and self.batch.is_delivered

    @property
    def is_overdue(self):
        return self.is_confirmed and not self.is_paid and self.due_date < timezone.now()

    @property
    def is_cancelled(self):
        return self.cancellation_time is not None

    @property
    def price_cents(self):
        # TODO Port to Django DB reduction functions if possible
        return sum(op.price_cents for op in self.order_product_set.all()) + self.shipping_and_handling_cents

    @property
    def shipping_and_handling_cents(self):
        return self.event.tickets_event_meta.shipping_and_handling_cents if self.requires_shipping else 0

    @property
    def formatted_shipping_and_handling(self):
        return format_price(self.shipping_and_handling_cents)

    @property
    def requires_shipping(self):
        # TODO do this in the database, too
        return any(op.product.requires_shipping for op in self.order_product_set.filter(count__gt=0))

    @property
    def formatted_price(self):
        return format_price(self.price_cents)

    @property
    def readable_state(self):
        if self.is_batched:
            return "Allocated into batch %d (%s)" % (self.batch.id, self.batch.readable_state)
        elif self.is_paid:
            return "Paid; awaiting allocation into batch"
        elif self.is_confirmed:
            if self.is_overdue:
                return "Confirmed; payment overdue since %s" % self.formatted_due_date
            else:
                return "Confirmed; payment due %s" % self.formatted_due_date
        else:
            return "Unconfirmed"

    @property
    def reference_number_base(self):
        return self.event.tickets_event_meta.reference_number_template.format(self.pk)

    def _make_reference_number(self):
        s = self.reference_number_base
        return s + str(-sum(int(x)*[7,3,1][i%3] for i, x in enumerate(s[::-1])) % 10)

    @property
    def formatted_reference_number(self):
        return "".join((i if (n+1) % 5 else i+" ") for (n, i) in enumerate(self.reference_number[::-1]))[::-1]

    @property
    def formatted_order_number(self):
        return "#{:05d}".format(self.pk)

    def clean_up_order_products(self):
        self.order_product_set.filter(count__lte=0).delete()

    def confirm_order(self):
        assert self.customer is not None
        assert not self.is_confirmed

        self.clean_up_order_products()

        self.reference_number = self._make_reference_number()
        self.confirm_time = timezone.now()
        self.save()

    def deconfirm_order(self):
        assert self.is_confirmed

        self.reference_number = self._make_reference_number()
        self.confirm_time = None
        self.save()

    def confirm_payment(self, payment_date=None, send_email=True):
        assert self.is_confirmed and not self.is_paid

        if payment_date is None:
            payment_date = date.today()

        self.payment_date = payment_date

        self.save()

        if 'lippukala' in settings.INSTALLED_APPS:
            self.lippukala_create_codes()

        if send_email:
            self.send_confirmation_message("payment_confirmation")

    def cancel(self, send_email=True):
        assert self.is_confirmed

        if 'lippukala' in settings.INSTALLED_APPS:
            self.lippukala_revoke_codes()

        self.cancellation_time = timezone.now()
        self.save()

        if send_email:
            self.send_confirmation_message("cancellation_notice")

    def uncancel(self, send_email=True):
        assert self.is_cancelled

        if 'lippukala' in settings.INSTALLED_APPS:
            self.lippukala_reinstate_codes()

        self.cancellation_time = None
        self.save()

        if send_email:
            self.send_confirmation_message("uncancellation_notice")

    @property
    def messages(self):
        seen = set()
        result = list()

        for op in self.order_product_set.all():
            md = op.product.mail_description

            if md is not None:
                if md not in seen:
                    seen.add(md)
                    result.append(md)

        return result

    @property
    def email_vars(self):
        return dict(order=self)

    @property
    def products_requiring_shipping(self):
        return self.order_product_set.filter(count__gt=0, product__requires_shipping=True)

    @property
    def due_date(self):
        meta = self.event.tickets_event_meta

        if self.confirm_time:
            return datetime.combine((self.confirm_time + timedelta(days=meta.due_days)).date(), dtime(23, 59, 59)).replace(tzinfo=timezone.tzlocal())
        else:
            return None

    @property
    def formatted_due_date(self):
        return format_date(self.due_date)

    @property
    def formatted_address(self):
        return u"{self.customer.name}\n{self.customer.address}\n{self.customer.zip_code} {self.customer.city}".format(self=self)

    @property
    def checkout_stamp(self):
        return "{0}{1:010.0f}".format(
            self.reference_number, # 6 digits
            mktime(self.start_time.timetuple()), # 10 digits
        )

    @property
    def checkout_message(self):
        return ", ".join(i.description for i in self.order_product_set.filter(count__gte=1))

    def checkout_mac(self, request):
        return compute_payment_request_mac(request, self)

    def checkout_return_url(self, request):
        return request.build_absolute_uri(url('payments_process_view', self.event.slug))

    @property
    def reservation_valid_until(self):
        return self.confirm_time + timedelta(seconds=self.event.tickets_event_meta.reservation_seconds) if self.confirm_time else None

    @property
    def contains_electronic_tickets(self):
        return self.order_product_set.filter(count__gt=0, product__electronic_ticket=True).exists()

    @property
    def lippukala_prefix(self):
        if 'lippukala' not in settings.INSTALLED_APPS:
            raise NotImplementedError('lippukala is not installed')

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
        if 'lippukala' not in settings.INSTALLED_APPS:
            raise NotImplementedError('lippukala is not installed')

        if not self.contains_electronic_tickets:
            return

        from lippukala.models import Code, Order as LippukalaOrder

        lippukala_order = LippukalaOrder.objects.create(
            address_text=self.formatted_address,
            free_text=self.event.tickets_event_meta.ticket_free_text,
            reference_number=self.reference_number,
        )

        for op in self.order_product_set.filter(count__gt=0, product__electronic_ticket=True):
            codes = [Code.objects.create(
                order=lippukala_order,
                prefix=self.lippukala_prefix,
                product_text=op.product.name,
            ) for i in xrange(op.count)]

        return lippukala_order, codes

    def lippukala_revoke_codes(self):
        if 'lippukala' not in settings.INSTALLED_APPS:
            raise NotImplementedError('lippukala is not installed')

        if not self.lippukala_order:
            return

        from lippukala.models import UNUSED, MANUAL_INTERVENTION_REQUIRED

        self.lippukala_order.code_set.filter(status=UNUSED).update(status=MANUAL_INTERVENTION_REQUIRED)

    def lippukala_reinstate_codes(self):
        if 'lippukala' not in settings.INSTALLED_APPS:
            raise NotImplementedError('lippukala is not installed')

        if not self.lippukala_order:
            return

        from lippukala.models import UNUSED, MANUAL_INTERVENTION_REQUIRED

        self.lippukala_order.code_set.filter(status=MANUAL_INTERVENTION_REQUIRED).update(status=UNUSED)

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

    def send_confirmation_message(self, msgtype):
        # don't fail silently, warn admins instead
        msgbcc = []
        meta = self.event.tickets_event_meta

        if meta.ticket_spam_email:
            msgbcc.append(meta.ticket_spam_email)

        for op in self.order_product_set.filter(count__gt=0):
            if op.product.notify_email:
                msgbcc.append(op.product.notify_email)

        attachments = []

        if msgtype == "payment_confirmation":
            if 'lippukala' in settings.INSTALLED_APPS and self.contains_electronic_tickets:
                from lippukala.printing import OrderPrinter

                printer = OrderPrinter(
                    print_logo_path=meta.print_logo_path,
                    print_logo_size_cm=meta.print_logo_size_cm,
                )
                printer.process_order(self.lippukala_order)
                attachments.append(('e-lippu.pdf', printer.finish(), 'application/pdf'))

                msgsubject = u"{self.event.name}: E-lippu ({self.formatted_order_number})".format(self=self)
                msgbody = render_to_string("tickets_confirm_payment.eml", self.email_vars)
            else:
                msgsubject = u"{self.event.name}: Tilausvahvistus ({self.formatted_order_number})".format(self=self)
                msgbody = render_to_string("tickets_confirm_payment.eml", self.email_vars)

        elif msgtype == "delivery_confirmation":
            msgsubject = u"{self.event.name}: Toimitusvahvistus ({self.formatted_order_number})".format(self=self)
            msgbody = render_to_string("tickets_confirm_delivery.eml", self.email_vars)

        elif msgtype == "cancellation_notice":
            msgsubject = u"{self.event.name}: Tilaus peruttu ({self.formatted_order_number})".format(self=self)
            msgbody = render_to_string("tickets_cancellation_notice.eml", self.email_vars)

        elif msgtype == "uncancellation_notice":
            msgsubject = u"{self.event.name}: Tilaus palautettu ({self.formatted_order_number})".format(self=self)
            msgbody = render_to_string("tickets_uncancellation_notice.eml", self.email_vars)

        else:
            raise NotImplementedError(msgtype)

        if settings.DEBUG:
            print msgbody

        message = EmailMessage(
            subject=msgsubject,
            body=msgbody,
            from_email=self.event.tickets_event_meta.contact_email,
            to=(self.customer.name_and_email,),
            bcc=msgbcc
        )

        for attachment in attachments:
            message.attach(*attachment)

        message.send(fail_silently=True)

    def render(self, c):
        render_receipt(self, c)

    def __unicode__(self):
        return u"#%s %s (%s)" % (
            self.pk,
            self.formatted_price,
            self.readable_state
        )

    class Meta:
        verbose_name = u'tilaus'
        verbose_name_plural = u'tilaukset'

    @classmethod
    def get_or_create_dummy(cls, event=None):
        if event is None:
            from core.models import Event

            meta, unused = TicketsEventMeta.get_or_create_dummy()
            event = meta.event

        customer, unused = Customer.get_or_create_dummy()
        t = timezone.now()

        return cls.objects.get_or_create(
            event=event,
            customer=customer,
        )

    @classmethod
    def get_unpaid_orders_to_cancel(cls, event, days=UNPAID_CANCEL_DAYS):
        deadline = timezone.now() - timedelta(days=days)
        return cls.objects.filter(
            event=event,
            confirm_time__lte=deadline,
            payment_date__isnull=True,
            cancellation_time__isnull=True,
        )

    @classmethod
    def cancel_unpaid_orders(cls, event, days=UNPAID_CANCEL_DAYS, send_email=False):
        orders = cls.get_unpaid_orders_to_cancel(event=event, days=days)
        count = orders.count()

        for order in orders:
            order.cancel(send_email=send_email)

        return count

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name="order_product_set")
    product = models.ForeignKey(Product, related_name="order_product_set")
    count = models.IntegerField(default=0)

    @property
    def target(self):
        return self.product

    @property
    def price_cents(self):
        return self.count * self.product.price_cents

    @property
    def formatted_price(self):
        return format_price(self.price_cents)

    @property
    def description(self):
        return u"%dx %s" % (
            self.count,
            self.product.name if self.product is not None else None
        )

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = u'tilausrivi'
        verbose_name_plural = u'tilausrivit'
