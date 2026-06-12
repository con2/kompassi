from __future__ import annotations

import logging
from functools import cached_property
from random import choice

from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

from kompassi.core.models.event import Event
from kompassi.core.models.one_time_code import (
    ONE_TIME_CODE_ALPHABET,
    ONE_TIME_CODE_LENGTH,
    ONE_TIME_CODE_STATE_CHOICES,
)
from kompassi.graphql_api.language import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGE_CODES, get_language_choices

logger = logging.getLogger(__name__)

CANCELLATION_REQUEST_SUBJECT = dict(
    fi="Tilauksen peruutuspyyntö",
    en="Order cancellation request",
)


class OrderCancellationToken(models.Model):
    """
    A one-time code sent to the email address of an order to confirm
    customer self-service cancellation of the order.

    NOTE: Order is partitioned by event, so we cannot have a foreign key to it.
    Instead, we use the same (event, order_id) pattern as Receipt.
    """

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="+",
    )

    order_id = models.UUIDField()

    code = models.CharField(max_length=63, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    state = models.CharField(
        max_length=8,
        default="valid",
        choices=ONE_TIME_CODE_STATE_CHOICES,
    )
    language = models.CharField(
        max_length=2,
        default=DEFAULT_LANGUAGE,
        choices=get_language_choices(),
    )

    class Meta:
        indexes = [
            models.Index(fields=["event", "order_id", "state"]),
        ]

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = "".join(choice(ONE_TIME_CODE_ALPHABET) for _ in range(ONE_TIME_CODE_LENGTH))

        return super().save(*args, **kwargs)

    @cached_property
    def order(self):
        """
        Direct the query to the correct partition.
        """
        from .order import Order

        return Order.objects.get(event=self.event, id=self.order_id)

    @property
    def confirmation_url(self) -> str:
        return (
            f"{settings.KOMPASSI_V2_BASE_URL}/{self.language}/{self.event.slug}"
            f"/orders/{self.order_id}/cancel/{self.code}"
        )

    def mark_used(self):
        if self.state != "valid":
            raise ValueError("Must be valid to mark used")

        self.used_at = timezone.now()
        self.state = "used"
        self.save(update_fields=["used_at", "state"])

    def revoke(self):
        if self.state != "valid":
            raise ValueError("Must be valid to revoke")

        self.used_at = timezone.now()
        self.state = "revoked"
        self.save(update_fields=["used_at", "state"])

    @property
    def message_language(self) -> str:
        """
        TODO Missing Swedish message template (see PendingReceipt.validate_language)
        """
        language = self.language.lower()
        if language == "sv" or language not in SUPPORTED_LANGUAGE_CODES:
            return DEFAULT_LANGUAGE

        return language

    def send(self):
        from kompassi.core.tasks import send_email

        order = self.order
        meta = order.meta
        event = self.event
        language = self.message_language

        deadline = order.cancellation_deadline
        if deadline is not None:
            deadline = deadline.astimezone(event.timezone)

        body = render_to_string(
            f"tickets_v2_cancellation_request_{language}.eml",
            dict(
                event_name=event.name,
                order_number=order.order_number,
                confirmation_url=self.confirmation_url,
                deadline=deadline,
                seller_name=event.organization.name,
                seller_email=meta.plain_contact_email,
                seller_business_id=event.organization.business_id,
            ),
        )

        subject = f"{event.name}: {CANCELLATION_REQUEST_SUBJECT[language]} ({order.formatted_order_number})"
        mail_domain = settings.DEFAULT_FROM_EMAIL.split("@", 1)[1].rstrip(">")
        from_email = f"{event.name} ({settings.KOMPASSI_INSTALLATION_NAME}) <{event.slug}-tickets@{mail_domain}>"
        reply_to = (contact_email,) if (contact_email := meta.contact_email) else ()
        to = (f"{order.first_name} {order.last_name} <{order.email}>",)

        send_email.delay(  # type: ignore
            subject=subject,
            body=body,
            from_email=from_email,
            reply_to=reply_to,
            to=to,
        )
