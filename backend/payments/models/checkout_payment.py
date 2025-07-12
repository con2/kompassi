from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import date
from functools import cached_property
from typing import TYPE_CHECKING
from uuid import uuid4

import requests
from django.conf import settings
from django.db import connection, models
from django.db.models import JSONField
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from core.utils.pkg_resources_compat import resource_string
from tickets.utils import format_price
from tickets_v2.optimized_server.utils.paytrail_hmac import calculate_hmac

from .payments_organization_meta import META_DEFAULTS

if TYPE_CHECKING:
    from tickets.models.LEGACY_TICKETSV1_order import Order

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


@dataclass
class PaymentsByPaymentMethod:
    provider: str

    num_new: int = 0
    num_ok: int = 0
    num_pending: int = 0
    num_fail: int = 0
    num_delayed: int = 0

    @property
    def num_total(self):
        return self.num_new + self.num_ok + self.num_pending + self.num_fail + self.num_delayed


@dataclass
class OrdersByPaymentStatus:
    new: int
    fail: int
    ok_after_fail: int
    ok_without_fail: int

    QUERY = resource_string(__name__, "queries/orders_by_payment_status.sql").decode("utf-8")

    @cached_property
    def total(self):
        return self.new + self.fail + self.ok_after_fail + self.ok_without_fail

    @property
    def new_percentage(self):
        return self.new / self.total * 100 if self.total else 0

    @property
    def fail_percentage(self):
        return self.fail / self.total * 100 if self.total else 0

    @property
    def ok_after_fail_percentage(self):
        return self.ok_after_fail / self.total * 100 if self.total else 0

    @property
    def ok_without_fail_percentage(self):
        return self.ok_without_fail / self.total * 100 if self.total else 0


class CheckoutPayment(models.Model):
    """
    Payment in the new Checkout API

    See https://checkoutfinland.github.io/psp-api/#/?id=request
    """

    organization = models.ForeignKey("core.Organization", on_delete=models.CASCADE)
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, blank=True, null=True)

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
        max_length=max(len(status) for (status, _) in CHECKOUT_STATUSES),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if self.event:
            self.organization = self.event.organization

        return super().save(*args, **kwargs)

    @classmethod
    def from_order(cls, order: Order):
        if order.event.start_time is None:
            raise ValueError("cannot perform Paytrail payment for event that has no start time")

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

        if order.customer is None:
            raise ValueError(f"Order {order} has no customer")

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
            items.append(
                {
                    "unitPrice": term.entrance_fee_cents,
                    "units": 1,
                    "vatPercentage": 0,
                    "productCode": f"{organization.slug}-entrance-{term.title}",
                    "description": "Liittymismaksu",
                    "deliveryDate": date.today().isoformat(),
                }
            )

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

    def perform_create_payment_request(self, request: HttpRequest):
        if not settings.DEBUG and self.meta.checkout_merchant == META_DEFAULTS["checkout_merchant"]:
            raise ValueError(f"Event {self.event} has testing merchant in production, please change this in admin")

        language = "FI" if get_language() == "fi" else "EN"

        body = {
            "stamp": str(self.stamp),
            "reference": self.reference,
            "amount": self.price_cents,
            "currency": "EUR",
            "language": language,
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
        response.raise_for_status()

        self.checkout_reference = result["reference"]
        self.checkout_transaction_id = result["transactionId"]
        self.save(update_fields=["checkout_reference", "checkout_transaction_id"])

        return result

    def process_checkout_response(self, response):
        """
        :param response: Query string params from Checkout

        NOTE: Signature must be already verified at this point
        """
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
        elif self.membership_fee_payment and self.status == "ok" and not self.membership_fee_payment.is_paid:
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
            return redirect("tickets_view", self.tickets_order.event.slug)
        elif self.membership_fee_payment:
            return redirect("core_organization_view", self.membership_fee_payment.term.organization.slug)
        else:
            raise NotImplementedError(f"Received payment without handler: {self.stamp}")

    @classmethod
    def get_payments_by_payment_method(cls, event):
        results: dict[str, PaymentsByPaymentMethod] = dict()

        for payment in cls.objects.filter(event=event):
            result = results.setdefault(payment.provider, PaymentsByPaymentMethod(provider=payment.provider))

            if payment.status == "new":
                result.num_new += 1
            elif payment.status == "ok":
                result.num_ok += 1
            elif payment.status == "pending":
                result.num_pending += 1
            elif payment.status == "fail":
                result.num_fail += 1
            elif payment.status == "delayed":
                result.num_delayed += 1
            else:
                raise NotImplementedError(payment.status)

        total_row = PaymentsByPaymentMethod(provider="Total")
        for result in results.values():
            total_row.num_new += result.num_new
            total_row.num_ok += result.num_ok
            total_row.num_pending += result.num_pending
            total_row.num_fail += result.num_fail
            total_row.num_delayed += result.num_delayed

        results_sorted = sorted(results.values(), key=lambda result: result.num_total, reverse=True)
        results_sorted.append(total_row)

        return results_sorted

    @classmethod
    def get_orders_by_payment_status(cls, event):
        with connection.cursor() as cursor:
            cursor.execute(OrdersByPaymentStatus.QUERY, [event.id])
            (one_row,) = cursor.fetchall()

        return OrdersByPaymentStatus(*one_row)
