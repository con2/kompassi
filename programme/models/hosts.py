# encoding: utf-8

from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify
from core.models import OneTimeCode


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


class Invitation(models.Model):
    """
    In order to add a Host to a Programme, the Programme Manager sends an invitation to the e-mail address of the
    Host. A Role is associated to the Invitation; when the Invitation is carried out and realized into a
    ProgrammeRole, the Role will be filled in from the Invitation.
    """

    email = models.CharField(max_length=1023)
    programme = models.ForeignKey('programme.Programme')
    role = models.ForeignKey('programme.Role')

    def __unicode__(self):
        return u'{email} ({programme})'.format(email=self.email, programme=self.programme)

    class Meta:
        verbose_name = _(u'invitation')
        verbose_name_plural = _(u'invitations')


# abuses OneTimeCode as these aren't "one-time"
class ProgrammeEditToken(OneTimeCode):
    programme = models.ForeignKey('programme.Programme')

    def render_message_subject(self, request):
        return u'{self.programme.event.name}: Ilmoita ohjelmanumerosi tiedot'.format(self=self)

    def render_message_body(self, request):
        from django.template import RequestContext
        from django.template.loader import render_to_string

        vars = dict(
            code=self,
            link=request.build_absolute_uri(url('programme_self_service_view', self.programme.event.slug, self.code))
        )

        return render_to_string('programme_self_service_message.eml', vars, context_instance=RequestContext(request, {}))

    def send(self, *args, **kwargs):
        kwargs.setdefault('from_email', self.programme.event.programme_event_meta.contact_email)
        super(ProgrammeEditToken, self).send(*args, **kwargs)
