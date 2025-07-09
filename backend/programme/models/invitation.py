from django.db import models, transaction
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from core.models import OneTimeCodeLite
from core.utils import url


class Invitation(OneTimeCodeLite):
    """
    In order to add a Host to a Programme, the Programme Manager sends an invitation to the e-mail address of the
    Host. A Role is associated to the Invitation; when the Invitation is carried out and realized into a
    ProgrammeRole, the Role will be filled in from the Invitation.
    """

    programme = models.ForeignKey(
        "programme.Programme",
        on_delete=models.CASCADE,
        verbose_name=_("Programme"),
    )

    role = models.ForeignKey(
        "programme.Role",
        on_delete=models.CASCADE,
        verbose_name=_("Role"),
    )

    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    extra_invites = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Extra invites"),
        help_text=_("The host may send this many extra invites to other hosts of the programme."),
    )

    sire = models.ForeignKey(
        "programme.ProgrammeRole",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Sire"),
        help_text=_(
            "The host that spawned this invitation. Sired invitations consume the extra invite quota of the sire."
        ),
        db_index=True,
        related_name="sired_invitations",
    )

    def __str__(self):
        return f"{self.email} ({self.programme})"

    @property
    def from_email(self):
        return self.programme.event.programme_event_meta.cloaked_contact_email

    @property
    def event(self):
        return self.programme.category.event if self.programme else None

    def render_message_subject(self, request):
        return f"{self.event.name}: Kutsu ohjelmanjärjestäjäksi"

    def render_message_body(self, request):
        event = self.event

        vars = dict(
            event=event,
            link=request.build_absolute_uri(url("programme:accept_invitation_view", event.slug, self.code)),
            meta=event.programme_event_meta,
            programme=self.programme,
        )

        return render_to_string("programme_invitation_message.eml", vars, request=request)

    def accept(self, person, sire=None):
        from .programme_role import ProgrammeRole

        with transaction.atomic():
            if sire and not sire.invitations_left:
                raise RuntimeError(f"No invitations left: {sire}")

            self.mark_used()

            programme_role = ProgrammeRole.from_invitation(self, person)
            programme_role.save()

        return programme_role

    @property
    def extra_invites_left(self):
        return self.extra_invites

    class Meta:
        verbose_name = _("invitation")
        verbose_name_plural = _("invitations")
