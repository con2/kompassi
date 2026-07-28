from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from django.db import models
from django_enum import EnumField

from kompassi.dimensions.models.scope import Scope
from kompassi.dimensions.models.universe import Universe

from .enums import MessageApp

if TYPE_CHECKING:
    from kompassi.core.models.event import Event


class MessageReplyTo(models.Model):
    """
    A reply-to address program managers may choose from when composing a Message.
    Managed on the Program V2 admin preferences page. Note the cloaked *from* address
    is unchanged (event.program_v2_event_meta.cloaked_contact_email) - only reply-to
    is selectable here.
    """

    universe: models.ForeignKey[Universe] = models.ForeignKey(
        Universe,
        on_delete=models.CASCADE,
        related_name="message_reply_tos",
    )

    app: EnumField[MessageApp] = EnumField(  # type: ignore
        MessageApp,
        default=MessageApp.PROGRAM,
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()

    id: int
    pk: int
    messages: models.QuerySet

    class Meta:
        ordering = ("universe", "name")

    def __str__(self):
        return f"{self.name} <{self.email}>"

    @cached_property
    def scope(self) -> Scope:
        return self.universe.scope

    @cached_property
    def event(self) -> Event:
        event = self.scope.event
        if event is None:
            raise ValueError(f"Scope of universe {self.universe} has no event")
        return event
