from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string

from core.models.event import Event
from event_log_v2.utils.monthly_partitions import UUID7Mixin
from graphql_api.language import DEFAULT_LANGUAGE, get_language_choices
from tickets_v2.optimized_server.utils.uuid7 import uuid7

from .enums import InvolvementApp

if TYPE_CHECKING:
    from forms.models.survey import Survey
    from program_v2.models.meta import ProgramV2EventMeta
    from program_v2.models.program import Program


class Invitation(UUID7Mixin, models.Model):
    """
    An Invitation is a way to invite a person to be Involved in an Event.
    Usually it is delivered via email, but it can also be delivered via other means.
    The email contains a link to accept the invitation.
    Accepting the invitation also involves answering a Survey.
    When the invitation is accepted, an Involvement is created.
    """

    id = models.UUIDField(default=uuid7, primary_key=True, editable=False)
    survey: models.ForeignKey[Survey] = models.ForeignKey(
        "forms.Survey",
        on_delete=models.CASCADE,
        related_name="invitations",
        help_text="When a user accepts this invitation, they will fill in this survey.",
    )

    program: models.ForeignKey[Program] = models.ForeignKey(
        "program_v2.Program",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="invitations",
    )

    # unused: used_at unset, involvement unset
    # used: used_at set, involvement set
    # revoked: used_at set, involvement unset
    used_at = models.DateTimeField(null=True, blank=True)
    involvement = models.OneToOneField(
        "involvement.Involvement",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="invitation",
    )

    created_by = models.ForeignKey(
        "auth.User",
        related_name="invitations_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    language = models.CharField(
        max_length=2,
        help_text="The language of the invitation. This is used to send the invitation in the correct language.",
        choices=get_language_choices(),
        default=DEFAULT_LANGUAGE,
    )
    email = models.EmailField(
        max_length=255,
        help_text="The email address of the person to invite. This is used to send the invitation.",
    )

    # cached_dimensions = models.JSONField(
    #     default=dict,
    #     blank=True,
    #     help_text="Dimensions to set on the Involvement created from this Invitation.",
    # )

    @cached_property
    def app(self) -> InvolvementApp:
        return InvolvementApp.from_app_name(self.survey.app)

    @cached_property
    def event(self) -> Event:
        return self.survey.event

    @cached_property
    def meta(self) -> ProgramV2EventMeta:
        if self.app != InvolvementApp.PROGRAM:
            raise NotImplementedError(f"Invitation not implemented for app {self.app}")

        return self.program.meta

    @property
    def accept_url(self) -> str:
        return f"{settings.KOMPASSI_V2_BASE_URL}/{self.event.slug}/invitations/{self.id}"

    @property
    def subject(self) -> str:
        match self.language:
            case "fi":
                return f"{self.event.name}: Kutsu ohjelmanjärjestäjäksi"
            case _:
                return f"{self.event.name}: Invitation to sign up as a program host"

    @property
    def body(self) -> str:
        vars = dict(
            event_name=self.event,
            link=self.accept_url,
            program_title=self.program.title,
        )

        match self.language:
            case "fi":
                return render_to_string("program_host_invitation_email/fi.eml", vars)
            case _:
                return render_to_string("program_host_invitation_email/en.eml", vars)

    def send(self):
        EmailMessage(
            subject=self.subject,
            body=self.body,
            from_email=self.meta.cloaked_contact_email,
            to=[self.email],
            reply_to=[self.meta.plain_contact_email],
        ).send()
