# encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from six import text_type

from core.csv_export import CsvExportMixin


class ProgrammeRole(models.Model, CsvExportMixin):
    person = models.ForeignKey('core.Person', on_delete=models.CASCADE, related_name='programme_roles')
    programme = models.ForeignKey('programme.Programme', on_delete=models.CASCADE)
    role = models.ForeignKey('programme.Role', on_delete=models.CASCADE)
    invitation = models.ForeignKey('programme.Invitation', on_delete=models.CASCADE, null=True, blank=True)

    # denormalized from programme.state
    is_active = models.BooleanField(default=True)

    extra_invites = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Extra invites'),
        help_text=_('The host may send this many extra invites to other hosts of the programme.'),
    )

    def clean(self):
        if self.role.require_contact_info and not (self.person.email or self.person.phone):
            from django.core.exceptions import ValidationError
            raise ValidationError('Contacts of this type require some contact info')

    def __str__(self):
        return '{person} ({programme})'.format(person=self.person, programme=self.programme)

    class Meta:
        verbose_name = _('Programme host')
        verbose_name_plural = _('Programme hosts')

    @classmethod
    def from_invitation(cls, invitation, person):
        """
        Return an unsaved new ProgrammeRole that gets its fields from `invitation` and `person`.
        """

        return cls(
            person=person,
            programme=invitation.programme,
            role=invitation.role,
            invitation=invitation,
            extra_invites=invitation.extra_invites
        )

    @classmethod
    def get_or_create_dummy(cls, programme=None, role=None):
        from core.models import Person
        from .role import Role
        from .programme import Programme

        person, unused = Person.get_or_create_dummy()

        if role is None:
            role, unused = Role.get_or_create_dummy()

        if programme is None:
            programme, unused = Programme.get_or_create_dummy()

        programme_role, created = ProgrammeRole.objects.get_or_create(
            person=person,
            programme=programme,
            defaults=dict(
                role=role,
            )
        )

        programme.apply_state()

        return programme_role, created

    @property
    def formatted_extra_invites(self):
        if self.extra_invites < 1:
            return text_type(self.extra_invites)
        else:
            return '{invites_used}/{invites}'.format(
                invites_used=self.extra_invites_used,
                invites=self.extra_invites,
            )

    @property
    def extra_invites_used(self):
        from .invitation import Invitation
        return self.sired_invitation_set.count()

    @property
    def extra_invites_left(self):
        return self.extra_invites - self.extra_invites_used

    @property
    def role_or_status(self):
        if self.programme.state in ['accepted', 'published']:
            return self.role.title
        else:
            return self.programme.get_state_display()

    @classmethod
    def get_csv_fields(cls, event):
        from core.models import Person
        from .programme import Programme

        return [
            (Person, 'surname'),
            (Person, 'first_name'),
            (Person, 'nick'),
            (Person, 'email'),
            (Person, 'phone'),
            (Programme, 'title'),
            (cls, 'role_or_status'),
        ]

    def get_csv_related(self):
        from core.models import Person
        from .programme import Programme

        return {
            Person: self.person,
            Programme: self.programme,
        }
