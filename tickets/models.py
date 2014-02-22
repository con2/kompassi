# encoding: utf-8
# vim: shiftwidth=4 expandtab

from datetime import datetime, timedelta, date
from datetime import time as dtime
from time import time, mktime

from django.db import models, IntegrityError
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone

from core.models import EventMetaBase
from payments.utils import compute_payment_request_mac

from .format import format_date, format_datetime, format_price
from .receipt import render_receipt


__all__ = [
    "School",
    "Batch",
    "Product",
    "Customer",
    "Order",
    "OrderProduct",
    "SHIPPING_AND_HANDLING_CENTS",
]


SHIPPING_AND_HANDLING_CENTS = getattr(settings, 'SHIPPING_AND_HANDLING_CENTS', 0)
DUE_DAYS = getattr(settings, 'DUE_DAYS', 7)
LOW_AVAILABILITY_THRESHOLD = getattr(settings, 'LOW_AVAILABILITY_THRESHOLD', 10)
DEFAULT_FINAL_DEATH_DAYS = 14 # XXX no longer used


class TicketsEventMeta(EventMetaBase):
    shipping_and_handling_cents = models.IntegerField(
        verbose_name=u'Toimituskulut (senttejä)',
        default=0,
    )

    due_days = model.IntegerField(
        verbose_name=u'Maksuaika (päiviä)'
        default=14,
    )




class Batch(models.Model):
    create_time = models.DateTimeField(auto_now=True)
    print_time = models.DateTimeField(null=True, blank=True)
    prepare_time = models.DateTimeField(null=True, blank=True)
    delivery_time = models.DateTimeField(null=True, blank=True)

    @property
    def is_printed(self):
        return self.print_time is not None

    @property
    def is_prepared(self):
        return self.prepare_time is not None

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
        elif self.is_prepared:
            return u"Prepared at %s; awaiting delivery" % format_date(self.prepare_time)
        elif self.is_printed:
            return u"Printed at %s; awaiting preparation" % format_date(self.print_time)
        else:
            return u"Awaiting print"

    @classmethod
    def create(cls, max_orders=100):
        # XXX concurrency disaster waiting to happen
        # solution: only I do the botching^Wbatching

        batch = cls()
        batch.save()

        orders = Order.objects.filter(
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
            if accepted >= max_orders:
                break

        return batch

    def render(self, c):
        for order in self.order_set.all():
            order.render(c)

    def cancel(self):
        for order in self.order_set.all():
            order.batch = None
            order.save()

        self.delete()

    def confirm_delivery(self, delivery_time=None):
        if delivery_time is None:
            delivery_time = timezone.now()

        self.delivery_time = delivery_time
        self.save()
        self.send_delivery_confirmation_messages()

    def send_delivery_confirmation_messages(self):
        for order in self.order_set.all():
            order.send_confirmation_message("toimitusvahvistus")

    def __unicode__(self):
        return u"#%d (%s)" % (
            self.pk,
            self.readable_state
        )

    class Meta:
        verbose_name_plural = "batches"

        permissions = (
            ("can_manage_batches", "Can manage batches"),
        )

class Product(models.Model):
    name = models.CharField(max_length=100)
    internal_description = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    mail_description = models.TextField(null=True, blank=True)
    sell_limit = models.IntegerField()
    price_cents = models.IntegerField()
    requires_shipping = models.BooleanField(default=True)
    available = models.BooleanField(default=True)
    ilmoitus_mail = models.CharField(max_length=100, null=True, blank=True)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ('ordering', 'id')

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
        return self.sell_limit - self.amount_sold

    @property
    def amount_sold(self):
        cnt = OrderProduct.objects.filter(product=self, order__confirm_time__isnull=False, order__cancellation_time__isnull=True).aggregate(models.Sum('count'))
        sm = cnt['count__sum']
        return sm if sm is not None else 0

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.formatted_price)

class School(models.Model):
    # REVERSE: order_set

    name = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    max_people = models.IntegerField()
    priority = models.IntegerField()

    @property
    def amount_placed(self):
        if self.id is None:
            return 0

        total = 0
        for order in self.order_set.filter(confirm_time__isnull=False, payment_date__isnull=False, cancellation_time__isnull=True):
            sleepy_op = order.order_product_set.get(product__name__icontains=u'majoitus')
            total += sleepy_op.count
        return total

    @property
    def amount_available(self):
        return self.max_people - self.amount_placed

    def __unicode__(self):
        return u"%s (%s/%s)" % (self.name, self.amount_placed, self.max_people)


class Customer(models.Model):
    # REVERSE: order = OneToOne(Order)
    first_name = models.CharField(max_length=100, verbose_name="Etunimi")
    last_name = models.CharField(max_length=100, verbose_name="Sukunimi")
    email = models.EmailField(verbose_name="Sähköpostiosoite")
    address = models.CharField(max_length=200, verbose_name="Katuosoite")
    zip_code = models.CharField(max_length=5, verbose_name="Postinumero")
    city = models.CharField(max_length=30, verbose_name="Postitoimipaikka")
    phone_number = models.CharField(max_length=30, null=True, blank=True, verbose_name="Puhelinnumero")

    def __unicode__(self):
        return self.name

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

class Order(models.Model):
    # REVERSE: order_product_set = ForeignKeyFrom(OrderProduct)

    customer = models.OneToOneField(Customer, null=True, blank=True)
    start_time = models.DateTimeField(auto_now=True)
    confirm_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.CharField(max_length=15, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    cancellation_time = models.DateTimeField(null=True, blank=True)
    batch = models.ForeignKey(Batch, null=True, blank=True)
    school = models.ForeignKey(School, null=True, blank=True)

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
        #return any(op.product.requires_shipping for op in self.order_product_set.filter(count__gt=0))

        # XXX PURKKA: tuote id:lla 8 on se viallinen Amuri-tuote johon unohtui toimitusbitti paalle
        return any((op.product.requires_shipping and op.product.id != 8) for op in self.order_product_set.filter(count__gt=0))

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
        return settings.REFERENCE_NUMBER_TEMPLATE.format(self.pk)

    @property
    def reference_number(self):
        s = self.reference_number_base
        return s + str(-sum(int(x)*[7,3,1][i%3] for i, x in enumerate(s[::-1])) % 10)

    @property
    def formatted_reference_number(self):
        return "".join((i if (n+1) % 5 else i+" ") for (n, i) in enumerate(self.reference_number[::-1]))[::-1]

    def confirm_order(self, send_email=True):
        assert self.customer is not None
        assert not self.is_confirmed

        self.order_product_set.filter(count__lte=0).delete()

        self.confirm_time = timezone.now()

        self.save()

        if send_email:
            self.send_confirmation_message("tilausvahvistus")

    def confirm_payment(self, payment_date=None, send_email=True):
        assert self.is_confirmed

        if payment_date is None:
            payment_date = date.today()

        self.payment_date = payment_date

        self.save()

        if send_email:
            self.send_confirmation_message("maksuvahvistus")

    def cancel(self):
        assert self.is_confirmed

        self.cancellation_time = timezone.now()
        self.save()
        self.send_confirmation_message('peruutus')

    @property
    def deduplicated_product_messages(self):
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
        return dict(
            order=self,
            products=self.order_product_set.all(),
            messages=self.deduplicated_product_messages,

            EVENT_NAME=settings.EVENT_NAME,
            EVENT_NAME_GENITIVE=settings.EVENT_NAME_GENITIVE,
            DEFAULT_FROM_EMAIL=settings.DEFAULT_FROM_EMAIL,
        )

    @property
    def order_confirmation_message(self):
        return render_to_string("email/confirm_order.eml", self.email_vars)

    @property
    def payment_confirmation_message(self):
        return render_to_string("email/confirm_payment.eml", self.email_vars)

    @property
    def delivery_confirmation_message(self):
        return render_to_string("email/confirm_delivery.eml", self.email_vars)

    @property
    def payment_reminder_message(self):
        return render_to_string("email/payment_reminder.eml", self.email_vars)

    @property
    def cancellation_notice_message(self):
        return render_to_string("email/cancellation_notice.eml", self.email_vars)

    @property
    def due_date(self):
        if self.confirm_time:
            return datetime.combine((self.confirm_time + timedelta(days=DUE_DAYS)).date(), dtime(23, 59, 59)).replace(tzinfo=timezone.get_default_timezone())
        else:
            return None

    @property
    def formatted_due_date(self):
        return format_date(self.due_date)

    @property
    def checkout_stamp(self):
        return "{0}{1:010.0f}".format(
            self.reference_number, # 6 digits
            mktime(self.start_time.timetuple()), # 10 digits
        )

    @property
    def checkout_message(self):
        return ", ".join(i.description for i in self.order_product_set.filter(count__gte=1))

    @property
    def checkout_mac(self):
        return compute_payment_request_mac(self)

    def send_confirmation_message(self, msgtype):
        # don't fail silently, warn admins instead
        for op in self.order_product_set.filter(count__gt=0):
            if op.product.ilmoitus_mail:
                msgbcc = (settings.TICKET_SPAM_EMAIL, op.product.ilmoitus_mail)
            else:
                msgbcc = (settings.TICKET_SPAM_EMAIL,)

        subject_vars = dict(
            EVENT_NAME=settings.EVENT_NAME,
            order_number=self.pk
        )

        if msgtype == "tilausvahvistus":
            msgsubject = "{EVENT_NAME}: Tilausvahvistus (#{order_number:04d})".format(**subject_vars)
            msgbody = self.order_confirmation_message
        elif msgtype == "maksuvahvistus":
            msgsubject = "{EVENT_NAME}: Maksuvahvistus (#{order_number:04d})".format(**subject_vars)
            msgbody = self.payment_confirmation_message
        elif msgtype == "toimitusvahvistus":
            msgsubject = "{EVENT_NAME}: Toimitusvahvistus (#{order_number:04d})".format(**subject_vars)
            msgbody = self.delivery_confirmation_message
        elif msgtype == "maksumuistutus":
            msgsubject = "{EVENT_NAME}: Maksumuistutus (#{order_number:04d})".format(**subject_vars)
            msgbody = self.payment_reminder_message
        elif msgtype == "peruutus":
            msgsubject = "{EVENT_NAME}: Tilaus peruuntunut (#{order_number:04d})".format(**subject_vars)
            msgbody = self.cancellation_notice_message
        else:
            raise NotImplementedError(msgtype)

        EmailMessage(
            subject=msgsubject,
            body=msgbody,
            to=(self.customer.name_and_email,),
            bcc=msgbcc
        ).send(fail_silently=True)

    def render(self, c):
        render_receipt(self, c)

    def __unicode__(self):
        return u"#%s %s (%s)" % (
            self.pk,
            self.formatted_price,
            self.readable_state
        )

    class Meta:
        permissions = (("can_manage_payments", "Can manage payments"),)

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
