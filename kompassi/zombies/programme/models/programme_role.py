from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.core.csv_export import CsvExportMixin
from kompassi.core.models import Event, Person

from .programme import Programme
from .role import Role


class ProgrammeRole(models.Model, CsvExportMixin):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="programme_roles")
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    # denormalized from kompassi.zombies.programme.state
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
    def role_or_status(self):
        if self.programme.state in ["accepted", "published"]:
            return self.role.title
        else:
            return self.programme.get_state_display()  # type: ignore

    @classmethod
    def get_csv_fields(cls, event):
        from kompassi.core.models import Person

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
        from kompassi.core.models import Person

        from .alternative_programme_form import AlternativeProgrammeForm
        from .programme import Programme
        from .role import Role

        return {
            Person: self.person,
            Programme: self.programme,
            Role: self.role,
            AlternativeProgrammeForm: self.programme.form_used,
        }
