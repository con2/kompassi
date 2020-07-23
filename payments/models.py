import hashlib
import json
import logging
from datetime import datetime, timezone, date
from uuid import uuid4

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect

from dateutil.parser import parse as parse_datetime
import requests

from core.models import EventMetaBase, GroupManagementMixin
from tickets.utils import format_price

from .utils import calculate_hmac


logger = logging.getLogger("kompassi")

CHECKOUT_API_BASE_URL = "https://api.checkout.fi"
CHECKOUT_PAYMENT_WALL_ORIGIN = "pay.checkout.fi"
CHECKOUT_STATUSES = [
    ("new", _("New")),
    ("ok", _("OK")),
    ("fail", _("Failed")),
    ("pending", _("Pending")),
    ("delayed", _("Delayed")),
]
META_DEFAULTS = dict(
    checkout_password="SAIPPUAKAUPPIAS",
    checkout_merchant="375917",
)


class PaymentsEventMeta(EventMetaBase):
    """
    Deprecated. PaymentsOrganizationMeta used instead.
    """
    checkout_password = models.CharField(max_length=255)
    checkout_merchant = models.CharField(max_length=255)
    checkout_delivery_date = models.CharField(max_length=9)

    @classmethod
    def get_or_create_dummy(cls, event):
        """
        Deprecated. But because it's used in an uwuton of places (that's, like, a thousand owotons),
        we jury-rig it to produce PaymentsOrganizationMeta instead.
        """
        unused, created = PaymentsOrganizationMeta.get_or_create_dummy(event.organization)
        return None, created


class PaymentsOrganizationMeta(models.Model):
    organization = models.OneToOneField('core.Organization', on_delete=models.CASCADE, primary_key=True)
    checkout_password = models.CharField(max_length=255)
    checkout_merchant = models.CharField(max_length=255)

    @classmethod
    def get_or_create_dummy(cls, organization=None):
        """
        Creates a POM with Checkout test merchant. Suitable for development, but try to use it in production and you'll get 500 ISE.
        """
        if organization is None:
            organization, uwused = Organization.get_or_create_dummy()

        return cls.objects.get_or_create(
            organization=organization,
            defaults=META_DEFAULTS,
        )

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
    organization = models.ForeignKey('core.Organization', on_delete=models.CASCADE)
    event = models.ForeignKey('core.Event', on_delete=models.CASCADE, blank=True, null=True)

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

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        if self.event:
            self.organization = self.event.organization

        return super().save(*args, **kwargs)

    @classmethod
    def from_order(cls, order):
        items = [
            {
                "unitPrice": order_product.product.price_cents,
                "units": order_product.count,
                "vatPercentage": 0,  # TODO make configurable
                "productCode": str(order_product.product.id),
                "deliveryDate": order.event.start_time.date().isoformat(),
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
            event=order.event,
            reference=order.reference_number,
            price_cents=order.price_cents,
            items=items,
            customer=customer,
        )

    @classmethod
    def from_membership_fee_payment(cls, membership_fee_payment):
        term = membership_fee_payment.term
        organization = term.organization
        person = membership_fee_payment.member.person

        items = [
            {
                "unitPrice": term.membership_fee_cents,
                "units": 1,
                "vatPercentage": 0,
                "productCode": f"{organization.slug}-membership-{term.title}",
                "description": f"Jäsenmaksu kaudelle {term.title}",
                "deliveryDate": term.start_date.isoformat(),
            }
        ]

        if term.entrance_fee_cents and membership_fee_payment.payment_type == "membership_fee_with_entrance_fee":
            items.append({
                "unitPrice": term.entrance_fee_cents,
                "units": 1,
                "vatPercentage": 0,
                "productCode": f"{organization.slug}-entrance-{term.title}",
                "description": f"Liittymismaksu",
                "deliveryDate": date.today().isoformat(),
            })

        customer = {
            "email": person.email,
            "firstName": person.first_name,
            "lastName": person.surname,
            "phone": person.normalized_phone_number or "",
        }

        return cls(
            organization=organization,
            reference=membership_fee_payment.reference_number,
            price_cents=membership_fee_payment.amount_cents,
            items=items,
            customer=customer,
        )

    @property
    def meta(self):
        return self.organization.payments_organization_meta

    @property
    def tickets_order(self):
        """
        Old webshop order for this payment, or None if this payment was not from the old webshop
        """
        if not hasattr(self, "_tickets_order"):
            from tickets.models import Order
            self._tickets_order = Order.objects.filter(reference_number=self.reference).first()

        return self._tickets_order

    @property
    def membership_fee_payment(self):
        if not hasattr(self, "_membership_fee_payment"):
            from membership.models import MembershipFeePayment
            self._membership_fee_payment = MembershipFeePayment.objects.filter(reference_number=self.reference).first()

        return self._membership_fee_payment

    def perform_create_payment_request(self, request):
        if not settings.DEBUG and self.meta.checkout_merchant == META_DEFAULTS["checkout_merchant"]:
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
        elif self.membership_fee_payment:
            if self.status == "ok" and not self.membership_fee_payment.is_paid:
                self.membership_fee_payment.confirm_payment(payment_method="checkout")

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

    def get_redirect(self):
        if self.tickets_order:
            # Old webshop order
            if self.status in ["ok", "pending", "delayed"]:
                return redirect("tickets_thanks_view", self.tickets_order.event.slug)
            else:
                return redirect("tickets_confirm_view", self.tickets_order.event.slug)
        elif self.membership_fee_payment:
            return redirect("core_organization_view", self.membership_fee_payment.term.organization.slug)
        else:
            # Not old webshop order (NOTE: should add handler, generic payments are bad m'kay)
            logger.warn("Received payment without webshop order or other handler: %s", payment.stamp)
            return redirect("core_frontpage_view")
