from __future__ import annotations

import logging
from functools import cached_property

from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.timezone import override as timezone_override

from kompassi.core.models.event import Event
from kompassi.core.models.one_time_code import ONE_TIME_CODE_STATE_CHOICES, OneTimeCodeMixin
from kompassi.graphql_api.language import DEFAULT_LANGUAGE, get_language_choices

from ..utils.mail import email_template_language, tickets_from_email

logger = logging.getLogger(__name__)

CANCELLATION_REQUEST_SUBJECT = dict(
    fi="Tilauksen peruutuspyyntö",
    en="Order cancellation request",
)


class OrderCancellationToken(models.Model, OneTimeCodeMixin):
    """
    A one-time code sent to the email address of an order to confirm
    customer self-service cancellation of the order.

    NOTE: Cannot extend the abstract OneTimeCode model because it requires a
    Person, and orders need not be associated with a user account. NOTE: Order
    is partitioned by event, so we cannot have a foreign key to it either.
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

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()

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

    def send_confirmation(self):
        """
        NOTE: Deliberately not OneTimeCodeMixin.send, which addresses the email
        via a Person and a request; this token has neither.
        """
        from kompassi.core.tasks import send_email

        order = self.order
        meta = order.meta
        event = self.event
        language = email_template_language(self.language)

        # NOTE: the |date template filter renders aware datetimes in the active
        # timezone, so the deadline must be rendered in the event timezone.
        with timezone_override(event.timezone):
            body = render_to_string(
                f"tickets_v2_cancellation_request_{language}.eml",
                dict(
                    event_name=event.name,
                    order_number=order.order_number,
                    confirmation_url=self.confirmation_url,
                    deadline=order.cancellation_deadline,
                    seller_name=event.organization.name,
                    seller_email=meta.plain_contact_email,
                    seller_business_id=event.organization.business_id,
                ),
            )

        subject = f"{event.name}: {CANCELLATION_REQUEST_SUBJECT[language]} ({order.formatted_order_number})"
        reply_to = (contact_email,) if (contact_email := meta.contact_email) else ()
        to = (f"{order.first_name} {order.last_name} <{order.email}>",)

        send_email.delay(  # type: ignore
            subject=subject,
            body=body,
            from_email=tickets_from_email(event),
            reply_to=reply_to,
            to=to,
        )
