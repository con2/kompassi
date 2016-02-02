# encoding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ProgrammeRole(models.Model):
    person = models.ForeignKey('core.Person')
    programme = models.ForeignKey('programme.Programme')
    role = models.ForeignKey('programme.Role')
    invitation = models.ForeignKey('programme.Invitation', null=True, blank=True)

    def clean(self):
        if self.role.require_contact_info and not (self.person.email or self.person.phone):
            from django.core.exceptions import ValidationError
            raise ValidationError('Contacts of this type require some contact info')

    def __unicode__(self):
        return self.role.title

    class Meta:
        verbose_name = u'ohjelmanpitäjän rooli'
        verbose_name_plural = u'ohjelmanpitäjien roolit'

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
