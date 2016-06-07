# encoding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


STATE_CHOICES = [
    ('pending', u'Odottaa hyväksyntää'),
    ('approved', u'Hyväksytty, odottaa toteutusta'),
    ('granted', u'Myönnetty'),
    ('rejected', u'Hylätty'),
]
STATE_CSS = dict(
    pending='label-warning',
    approved='label-primary',
    granted='label-success',
    rejected='label-danger',
)


class GrantedPrivilege(models.Model):
    privilege = models.ForeignKey('access.Privilege', related_name='granted_privileges')
    person = models.ForeignKey('core.Person', related_name='granted_privileges')
    state = models.CharField(default='granted', max_length=8, choices=STATE_CHOICES)

    granted_at = models.DateTimeField(auto_now_add=True)

    @property
    def state_css(self):
        return STATE_CSS[self.state]

    def __unicode__(self):
        return u'{person_name} - {privilege_title}'.format(
            person_name=self.person.full_name if self.person else None,
            privilege_title=self.privilege.title if self.privilege else None,
        )

    class Meta:
        verbose_name = _('granted privilege')
        verbose_name_plural = _('granted privileges')

        unique_together = [('privilege', 'person')]
