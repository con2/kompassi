import hashlib
import json
import logging
from datetime import datetime, timezone
from uuid import uuid4

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from dateutil.parser import parse as parse_datetime
import requests

from core.models import EventMetaBase
from tickets.utils import format_price

from .utils import calculate_hmac


logger = logging.getLogger("kompassi")

CHECKOUT_API_BASE_URL = "https://api.checkout.fi"
CHECKOUT_STATUSES = [
    ("new", _("New")),
    ("ok", _("OK")),
    ("fail", _("Failed")),
    ("pending", _("Pending")),
    ("delayed", _("Delayed")),
]
EVENT_META_DEFAULTS = dict(
    checkout_password="SAIPPUAKAUPPIAS",
    checkout_merchant="375917",
    checkout_delivery_date="20130914",
)


class PaymentsEventMeta(EventMetaBase):
    checkout_password = models.CharField(max_length=255)
    checkout_merchant = models.CharField(max_length=255)
    checkout_delivery_date = models.CharField(max_length=9)

    @classmethod
    def get_or_create_dummy(cls, event=None):
        from django.contrib.auth.models import Group
        from core.models import Event

        if event is None:
            event, unused = Event.get_or_create_dummy()

        group, = PaymentsEventMeta.get_or_create_groups(event, ["admins"])

        return cls.objects.get_or_create(event=event, defaults=dict(
            EVENT_META_DEFAULTS,
            admin_group=group,
        ))

    def get_checkout_params(self, method="POST", t=None):
        if t is None:
            t = datetime.now(timezone.utc)

        return {
            "checkout-account": self.checkout_merchant,
            "checkout-algorithm": "sha256",
            "checkout-method": method,
            "checkout-nonce": str(uuid4()),
            "checkout-timestamp": t.isoformat(),
        }

    @property
    def normalized_checkout_delivery_date(self):
        """
        In the Olden Days of PHP and Joose the delivery date was encoded as YYYYMMDD.
        In the Modern Days of Typescript and Vesse the delivery date is encoded YYYY-MM-DD.
        This returns whichever is stored as YYYY-MM-DD.
        """
        if not self.checkout_delivery_date:
            return None

        return parse_datetime(self.checkout_delivery_date).strftime("%Y-%m-%d")

    class Meta:
        verbose_name = "tapahtuman maksunvälitystiedot"
        verbose_name_plural = "tapahtuman maksunvälitystiedot"


class Payment(models.Model):
    """
    Legacy payment, not used by v2 api
    """
    event = models.ForeignKey('core.Event', on_delete=models.CASCADE)

    VERSION = models.CharField(max_length=4)
    STAMP = models.CharField(max_length=20)
    REFERENCE = models.CharField(max_length=20)
    PAYMENT = models.CharField(max_length=20)
    STATUS = models.IntegerField()
    ALGORITHM = models.IntegerField()
    MAC = models.CharField(max_length=32)


class CheckoutPayment(models.Model):
    """
    Payment in the new Checkout API

    See https://checkoutfinland.github.io/psp-api/#/?id=request
    """
    event = models.ForeignKey('core.Event', on_delete=models.CASCADE)

    # Fields sent in Create Payment request
    stamp = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    reference = models.TextField(editable=False)
    price_cents = models.IntegerField(editable=False)
    items = JSONField(editable=False)
    customer = JSONField(editable=False)

    # Fields extracted from Create Payment response
    checkout_reference = models.TextField(editable=False, blank=True)
    checkout_transaction_id = models.TextField(editable=False, blank=True)

    # Fields extracted from redirect or callback
    provider = models.TextField(editable=False, blank=True)
    status = models.CharField(
        default="new",
        editable=False,
        choices=CHECKOUT_STATUSES,
        max_length=max(len(status) for (status, _) in CHECKOUT_STATUSES)
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def from_order(cls, order):
        items = [
            {
                "unitPrice": order_product.product.price_cents,
                "units": order_product.count,
                "vatPercentage": 0,  # TODO make configurable
                "productCode": str(order_product.product.id),
                "deliveryDate": order.event.payments_event_meta.normalized_checkout_delivery_date
            }
            for order_product in order.order_product_set.all()
            if order_product.count > 0
        ]

        customer = {
            "email": order.customer.email,
            "firstName": order.customer.first_name,
            "lastName": order.customer.last_name,
            "phone": order.customer.normalized_phone_number or "",
        }

        return cls(
            stamp=uuid4(),
            event=order.event,
            reference=order.reference_number,
            price_cents=order.price_cents,
            items=items,
            customer=customer,
        )

    @property
    def meta(self):
        return self.event.payments_event_meta

    @property
    def tickets_order(self):
        """
        Old webshop order for this payment, or None if this payment was not from the old webshop
        """
        if not hasattr(self, "_tickets_order"):
            from tickets.models import Order
            self._tickets_order = Order.objects.filter(reference_number=self.reference).first()

        return self._tickets_order

    def perform_create_payment_request(self, request):
        if not settings.DEBUG and self.meta.checkout_merchant == EVENT_META_DEFAULTS["checkout_merchant"]:
            raise ValueError(f"Event {self.event} has testing merchant in production, please change this in admin")

        body = {
            "stamp": str(self.stamp),
            "reference": self.reference,
            "amount": self.price_cents,
            "currency": "EUR",
            "language": "FI",  # TODO user's language
            "items": self.items,
            "customer": self.customer,
            "redirectUrls": {
                "success": request.build_absolute_uri(reverse("payments_checkout_success_view")),
                "cancel": request.build_absolute_uri(reverse("payments_checkout_cancel_view")),
            },

        }

        callback_urls = {
            "success": request.build_absolute_uri(reverse("payments_checkout_success_callback")),
            "cancel": request.build_absolute_uri(reverse("payments_checkout_cancel_callback")),
        }
        if "localhost" not in callback_urls["success"]:
            body["callbackUrls"] = callback_urls

        body = json.dumps(body)

        headers = self.meta.get_checkout_params()
        headers["signature"] = calculate_hmac(self.meta.checkout_password, headers, body)
        headers["content-type"] = "application/json"

        url = f"{CHECKOUT_API_BASE_URL}/payments"

        response = requests.post(url, headers=headers, data=body)
        result = response.json()
        logger.debug("perform_create_payment_request response %r", result)
        response.raise_for_status()

        self.checkout_reference = result["reference"]
        self.checkout_transaction_id = result["transactionId"]
        self.save()

        return result

    def process_checkout_response(self, response):
        """
        :param response: Query string params from Checkout

        NOTE: Signature must be already verified at this point
        """
        logger.debug("process_checkout_response %r", response)

        for key, expected_value in {
            "checkout-account": self.meta.checkout_merchant,
            "checkout-algorithm": "sha256",
            "checkout-amount": str(self.price_cents),
            "checkout-stamp": str(self.stamp),
            "checkout-reference": self.reference,  # NOTE! Not checkout_reference!
            "checkout-transaction-id": self.checkout_transaction_id,
        }.items():
            actual_value = response[key]
            if actual_value != expected_value:
                logger.warning(
                    "Value of %r in response for payment of stamp %s does not match (expected %r, got %r)",
                    key,
                    self.stamp,
                    expected_value,
                    actual_value,
                )

        self.status = response["checkout-status"]
        self.provider = response["checkout-provider"]
        self.save()

        if self.tickets_order:
            if self.status == "ok" and not self.tickets_order.is_paid:
                self.tickets_order.confirm_payment()

    def admin_get_customer_email(self):
        try:
            return self.customer["email"]
        except (IndexError, KeyError, ValueError):
            return None
    admin_get_customer_email.short_description = "Customer E-mail"

    def admin_get_formatted_amount(self):
        if self.price_cents is None:
            return None

        return format_price(self.price_cents)
    admin_get_formatted_amount.short_description = "Amount"
    admin_get_formatted_amount.admin_order_field = "price_cents"
