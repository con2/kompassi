from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import cached_property

from django.conf import settings
from django.db import models

from core.models.contact_email_mixin import ContactEmailMixin, contact_email_validator
from core.models.event_meta_base import EventMetaBase
from core.models.person import Person

from ..optimized_server.models.enums import PaymentProvider, PaymentStatus

logger = logging.getLogger("kompassi")


class TicketsV2EventMeta(ContactEmailMixin, EventMetaBase):
    provider_id = models.SmallIntegerField(
        choices=[(x.value, x.name) for x in PaymentProvider],
        default=PaymentProvider.NONE,
        verbose_name="Payment provider",
    )

    # NOTE SUPPORTED_LANGUAGES
    terms_and_conditions_url_en = models.TextField(default="", blank=True)
    terms_and_conditions_url_fi = models.TextField(default="", blank=True)
    terms_and_conditions_url_sv = models.TextField(default="", blank=True)

    contact_email = models.CharField(
        max_length=255,
        blank=True,
        validators=[contact_email_validator],
        help_text="Foo Bar &lt;foo.bar@example.com&gt;",
    )

    use_cbac = True

    def __str__(self):
        return str(self.event)

    def ensure_partitions(self):
        from .order import Order
        from .payment_stamp import PaymentStamp
        from .receipt import Receipt
        from .ticket import Ticket

        Order.ensure_partition(self.event)
        Ticket.ensure_partition(self.event)
        PaymentStamp.ensure_partition(self.event)
        Receipt.ensure_partition(self.event)

    @property
    def scope(self):
        return self.event.scope

    def get_available_products(self):
        from core.utils.time_utils import get_objects_within_period

        from .product import Product

        return get_objects_within_period(
            Product,
            start_field_name="available_from",
            end_field_name="available_until",
            event_id=self.event_id,
        )

    @property
    def have_available_products(self):
        return self.get_available_products().exists()

    @property
    def tickets_url(self):
        return f"{settings.KOMPASSI_V2_BASE_URL}/{self.event.slug}/tickets"

    def reticket(self):
        """
        After changing quotas of a product, this method can be used to
        assign tickets to orders having that product.

        Must be called in a transaction.
        """
        from .order import Order
        from .product import Product
        from .quota import Quota, QuotaCounters
        from .ticket import Ticket

        logger.info("Reticketing event %s", self.event)

        quota_counters = QuotaCounters.get_for_event(self.event_id, None)
        products_by_id = {
            str(product.id): product.superseded_by if product.superseded_by else product
            for product in Product.objects.filter(event=self.event).prefetch_related("quotas")
        }
        orders = Order.objects.filter(
            event=self.event_id,
            cached_status__lte=PaymentStatus.PAID.value,
        )

        # May the Transaction be with us.
        Ticket.objects.filter(event=self.event_id).delete()
        Ticket.objects.bulk_create(
            (
                Ticket(
                    event_id=self.event_id,
                    quota=quota,
                    order_id=order.id,
                )
                for order in orders
                if order.cached_status == PaymentStatus.PAID
                for product_id, quantity in order.product_data.items()
                for quota in products_by_id[product_id].quotas.all()
                for _ in range(quantity)
            ),
            batch_size=400,
        )

        for quota_id, counters in quota_counters.items():
            quota = Quota.objects.get(id=quota_id)
            quota.set_quota(counters.count_total)

    @cached_property
    def provider(self):
        from ..providers.null import NULL_PROVIDER
        from ..providers.paytrail import PAYTRAIL_PROVIDER

        match self.provider_id:
            case PaymentProvider.NONE:
                return NULL_PROVIDER
            case PaymentProvider.PAYTRAIL:
                return PAYTRAIL_PROVIDER
            case _:
                raise NotImplementedError(f"Unsupported provider_id: {self.provider_id}")


@dataclass
class TicketsV2ProfileMeta:
    """
    No need for an actual model for now. This serves as a stand-in for GraphQL.
    """

    person: Person
