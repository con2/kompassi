# encoding: utf-8

from django.db import models
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify, url
from core.models import OneTimeCode, OneTimeCodeLite


class Role(models.Model):
    title = models.CharField(max_length=1023)
    require_contact_info = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'role')
        verbose_name_plural = _(u'roles')
        ordering = ['title']

    @classmethod
    def get_or_create_dummy(cls):
        return cls.objects.get_or_create(
            title=u'Overbaron',
            require_contact_info=False
        )


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
    def get_or_create_dummy(cls, programme=None):
        from core.models import Person

        person, unused = Person.get_or_create_dummy()
        role, unused = Role.get_or_create_dummy()

        if programme is None:
            programme, unused = Programme.get_or_create_dummy()

        ProgrammeRole.objects.get_or_create(
            person=person,
            programme=programme,
            role=role,
        )


class Invitation(OneTimeCodeLite):
    """
    In order to add a Host to a Programme, the Programme Manager sends an invitation to the e-mail address of the
    Host. A Role is associated to the Invitation; when the Invitation is carried out and realized into a
    ProgrammeRole, the Role will be filled in from the Invitation.
    """

    programme = models.ForeignKey('programme.Programme',
        verbose_name=_(u'Programme'),
    )

    role = models.ForeignKey('programme.Role',
        verbose_name=_(u'Role'),
    )

    created_by = models.ForeignKey('auth.User',
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return u'{email} ({programme})'.format(email=self.email, programme=self.programme)

    @property
    def event(self):
        return self.programme.category.event if self.programme else None

    def render_message_subject(self, request):
        return u'{event_name}: Kutsu ohjelmanjärjestäjäksi'.format(
            event_name=self.event.name,
        )

    def render_message_body(self, request):
        event = self.event

        vars = dict(
            event=event,
            link=request.build_absolute_uri(url('programme_accept_invitation_view', event.slug, self.code)),
            meta=event.programme_event_meta,
            programme=self.programme,
        )

        return render_to_string('programme_invitation_message.eml', vars, request=request)

    def accept(self, person):
        self.mark_used()

        programme_role = ProgrammeRole(
            programme=self.programme,
            role=self.role,
            person=person,
            invitation=self,
        )
        programme_role.save()
        return programme_role

    class Meta:
        verbose_name = _(u'invitation')
        verbose_name_plural = _(u'invitations')
