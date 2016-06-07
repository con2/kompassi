# encoding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class GroupPrivilege(models.Model):
    privilege = models.ForeignKey('access.Privilege', related_name='group_privileges')
    group = models.ForeignKey('auth.Group', related_name='group_privileges')
    event = models.ForeignKey('core.Event', null=True, blank=True, related_name='group_privileges')

    def __unicode__(self):
        return u'{group_name} - {privilege_title}'.format(
            group_name=self.group.name if self.group else None,
            privilege_title=self.privilege.title if self.privilege else None,
        )

    class Meta:
        verbose_name = _('group privilege')
        verbose_name_plural = _('group privileges')

        unique_together = [('privilege', 'group')]
