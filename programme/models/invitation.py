# encoding: utf-8

from django.db import models
from django.template.loader import render_to_string
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from core.utils import url
from core.models import OneTimeCodeLite


@python_2_unicode_compatible
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

    def __str__(self):
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
        from .programme_role import ProgrammeRole

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