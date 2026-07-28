from __future__ import annotations

import logging
from functools import cached_property
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models, transaction
from django.utils.timezone import now
from django_enum import EnumField

from kompassi.dimensions.filters import DimensionFilters
from kompassi.dimensions.models.scope import Scope
from kompassi.dimensions.models.universe import Universe
from kompassi.tickets_v2.optimized_server.utils.uuid7 import uuid7, uuid7_to_datetime

from .enums import MessageApp, MessageDispatch, MessageState
from .recipient_filters import validate_recipient_filters

if TYPE_CHECKING:
    from kompassi.core.models.event import Event
    from kompassi.involvement.models.involvement import Involvement

    from .message_reply_to import MessageReplyTo

logger = logging.getLogger(__name__)


class Message(models.Model):
    """
    A message that program managers can send to program offerers/hosts (and, in the
    future, other Involvement-based recipients). See docs/plans or the messages_v2
    app for the full design; in short: draft -> active (sent) -> optionally expired.
    """

    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)

    universe: models.ForeignKey[Universe] = models.ForeignKey(
        Universe,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    app: EnumField[MessageApp] = EnumField(  # type: ignore
        MessageApp,
        default=MessageApp.PROGRAM,
    )

    subject = models.CharField(max_length=255, blank=True, default="")
    body = models.TextField(blank=True, default="")

    dispatch: EnumField[MessageDispatch] = EnumField(  # type: ignore
        MessageDispatch,
        default=MessageDispatch.PER_PERSON,
    )

    reply_to: models.ForeignKey[MessageReplyTo] | None = models.ForeignKey(
        "messages_v2.MessageReplyTo",
        on_delete=models.SET_NULL,
        related_name="messages",
        null=True,
        blank=True,
    )

    # list[list[{dimension: str, values: list[str] | None}]] - OR of AND-groups, validated
    # by validate_recipient_filters() before save (see clean_recipient_filters()).
    recipient_filters = models.JSONField(default=list, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )

    recipients: models.QuerySet

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.subject or f"Message {self.pk}"

    @cached_property
    def created_at(self):
        return uuid7_to_datetime(self.id)

    @cached_property
    def scope(self) -> Scope:
        return self.universe.scope

    @cached_property
    def event(self) -> Event:
        event = self.scope.event
        if event is None:
            raise ValueError(f"Scope of universe {self.universe} has no event")
        return event

    @property
    def state(self) -> MessageState:
        if self.sent_at is None:
            return MessageState.DRAFT
        if self.expired_at is not None and self.expired_at <= now():
            return MessageState.EXPIRED
        return MessageState.ACTIVE

    def clean_recipient_filters(self):
        """
        Call before save whenever recipient_filters may have come from untrusted input.
        """
        self.recipient_filters = validate_recipient_filters(self.recipient_filters)

    def resolve_involvements(self) -> models.QuerySet[Involvement]:
        """
        Involvements matching any of the OR-of-AND recipient filter groups.
        """
        from kompassi.involvement.models.involvement import Involvement

        base = self.universe.all_involvements.all()

        if not self.recipient_filters:
            return base.none()

        involvement_ids: set[int] = set()
        for group in self.recipient_filters:
            filters = {item["dimension"]: item.get("values") or ["*"] for item in group}
            involvement_ids.update(DimensionFilters(filters=filters).filter(base).values_list("id", flat=True))

        return Involvement.objects.filter(id__in=involvement_ids)

    def resolve_recipient_count(self) -> int:
        involvements = self.resolve_involvements()

        if self.dispatch == MessageDispatch.PER_INVOLVEMENT:
            return involvements.count()

        return involvements.values("person_id").distinct().count()

    @transaction.atomic
    def send(self):
        from ..tasks import send_message

        if self.sent_at is None:
            self.sent_at = now()
            self.save(update_fields=["sent_at"])

        send_message.delay(str(self.id))

    def expire(self):
        self.expired_at = now()
        self.save(update_fields=["expired_at"])
