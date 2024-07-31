from __future__ import annotations

from typing import Self

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.csv_export import CsvExportMixin
from core.models import Event, Person

from .invitation import Invitation
from .programme import Programme
from .role import Role


class ProgrammeRole(models.Model, CsvExportMixin):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="programme_roles")
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, null=True, blank=True)

    # denormalized from programme.state
    is_active = models.BooleanField(default=True)

    extra_invites = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Extra invites"),
        help_text=_("The host may send this many extra invites to other hosts of the programme."),
    )

    override_perks = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Override perks"),
        help_text=_("If set, overrides the perks set in the role."),
    )

    sired_invitations: models.QuerySet[Invitation]

    @property
    def perks(self) -> dict[str, int | bool]:
        return self.override_perks or self.role.perks

    def clean(self):
        if self.role.require_contact_info and not (self.person.email or self.person.phone):
            from django.core.exceptions import ValidationError

            raise ValidationError("Contacts of this type require some contact info")

    def __str__(self):
        return f"{self.person} ({self.programme})"

    class Meta:
        verbose_name = _("Programme host")
        verbose_name_plural = _("Programme hosts")
        unique_together = [("person", "programme")]

    @classmethod
    def from_invitation(cls, invitation: Invitation, person: Person) -> Self:
        """
        Return an unsaved new ProgrammeRole that gets its fields from `invitation` and `person`.
        """

        return cls(
            person=person,
            programme=invitation.programme,
            role=invitation.role,
            invitation=invitation,
            extra_invites=invitation.extra_invites,
        )

    @classmethod
    def get_or_create_dummy(
        cls,
        programme: Programme | None = None,
        person: Person | None = None,
        role: Role | None = None,
        event: Event | None = None,
    ):
        if event is None:
            event, unused = Event.get_or_create_dummy()

        if person is None:
            person, unused = Person.get_or_create_dummy()

        if role is None:
            role, unused = Role.get_or_create_dummy(event=event)

        if programme is None:
            programme, unused = Programme.get_or_create_dummy(event=event)

        programme_role, created = ProgrammeRole.objects.get_or_create(
            person=person,
            programme=programme,
            defaults=dict(
                role=role,
            ),
        )

        programme.apply_state()

        return programme_role, created

    @property
    def formatted_extra_invites(self):
        if self.extra_invites < 1:
            return str(self.extra_invites)
        else:
            return f"{self.extra_invites_used}/{self.extra_invites}"

    @property
    def extra_invites_used(self):
        return self.sired_invitations.count()

    @property
    def extra_invites_left(self):
        return self.extra_invites - self.extra_invites_used

    @property
    def role_or_status(self):
        if self.programme.state in ["accepted", "published"]:
            return self.role.title
        else:
            return self.programme.get_state_display()  # type: ignore

    @classmethod
    def get_csv_fields(cls, event):
        from core.models import Person

        from .alternative_programme_form import AlternativeProgrammeForm
        from .programme import Programme
        from .role import Role

        return [
            (Person, "surname"),
            (Person, "first_name"),
            (Person, "nick"),
            (Person, "email"),
            (Person, "phone"),
            (Person, "discord_handle"),
            (Person, "may_send_info"),
            (Programme, "title"),
            (Programme, "get_state_display"),
            (Role, "title"),
            (AlternativeProgrammeForm, "title"),
        ]

    def get_csv_related(self):
        from core.models import Person

        from .alternative_programme_form import AlternativeProgrammeForm
        from .programme import Programme
        from .role import Role

        return {
            Person: self.person,
            Programme: self.programme,
            Role: self.role,
            AlternativeProgrammeForm: self.programme.form_used,
        }
