from __future__ import annotations

from functools import cached_property
from uuid import UUID

from django.db import models

from kompassi.core.models.event import Event
from kompassi.event_log_v2.utils.monthly_partitions import UUID7Mixin, uuid7

from ..optimized_server.models.enums import PaymentProvider, PaymentStampType, PaymentStatus
from ..utils.event_partitions import EventPartitionsMixin
from .order import Order


class PaymentStamp(EventPartitionsMixin, UUID7Mixin, models.Model):
    """
    Payment stamps are created at various stages of payment processing.
    The table is strictly insert only; no updates or deletes will ever be made.

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
            "The correlation ID ties together the payment stamps related to the same payment attempt. "
            "For Paytrail, this is what they call 'stamp'."
        ),
    )

    provider_id = models.SmallIntegerField(
        choices=[(p.value, p.name) for p in PaymentProvider],
    )
    type = models.SmallIntegerField(
        choices=[(t.value, t.name) for t in PaymentStampType],
    )
    status = models.SmallIntegerField(
        choices=[(s.value, s.name) for s in PaymentStatus],
    )

    data = models.JSONField(
        help_text=(
            "What we sent to or received from the payment provider_id. "
            "Sensitive details such as API credentials, PII etc. may be redacted. "
            "Also fields lifted to relational fields need not be repeated here."
        )
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

    @property
    def provider(self):
        return PaymentProvider(self.provider_id)

    def as_paytrail_payment_callback(self):
        """
        If this payment stamp is a Paytrail payment callback or redirect, return its parsed payload.
        Otherwise raise ValueError.
        """
        from ..optimized_server.providers.paytrail import PaymentCallback

        if self.provider == PaymentProvider.PAYTRAIL and self.type in (
            PaymentStampType.PAYMENT_REDIRECT,
            PaymentStampType.PAYMENT_CALLBACK,
        ):
            pass
        else:
            raise ValueError("Not a Paytrail payment callback")

        return PaymentCallback.model_validate(self.data)
