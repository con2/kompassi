from __future__ import annotations

from django.db import models

from .message import Message
from .message_body import MessageBody


class MessageRecipient(models.Model):
    """
    A per-recipient sent record. Doubles as the idempotency guard (a person/involvement
    is only ever sent a given Message once) and as the immutable rendered snapshot that
    the recipient sees in their profile - edits to Message after this row exists never
    change what this row shows.
    """

    message: models.ForeignKey[Message] = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="recipients",
    )
    person = models.ForeignKey(
        "core.Person",
        on_delete=models.CASCADE,
        related_name="received_messages",
    )
    # Set for PER_INVOLVEMENT dispatch (the involvement this copy was sent for) and for
    # auto-send (the involvement whose change triggered the send); null for a PER_PERSON
    # send that groups multiple involvements into a single copy.
    involvement = models.ForeignKey(
        "involvement.Involvement",
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
    )

    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body: models.ForeignKey[MessageBody] = models.ForeignKey(
        MessageBody,
        on_delete=models.CASCADE,
        related_name="+",
    )

    sent_at = models.DateTimeField(auto_now_add=True)

    # Snapshot of the involvement's cached_dimensions at send time, so the profile view
    # can offer DimensionFilters by event/type without joining back to Involvement.
    cached_dimensions = models.JSONField(default=dict, blank=True)

    id: int
    pk: int
    body_id: int

    class Meta:
        ordering = ("-sent_at",)
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(
                fields=["message", "person"],
                condition=models.Q(involvement__isnull=True),
                name="messages_v2_messagerecipient_unique_person",
            ),
            models.UniqueConstraint(
                fields=["message", "involvement"],
                condition=models.Q(involvement__isnull=False),
                name="messages_v2_messagerecipient_unique_involvement",
            ),
        ]

    def __str__(self):
        return f"{self.message} -> {self.person} ({self.email})"
