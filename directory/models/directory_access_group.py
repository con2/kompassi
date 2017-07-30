from django.db import models
from django.utils.translation import ugettext_lazy as _


class DirectoryAccessGroup(models.Model):
    organization = models.ForeignKey('core.Organization')
    group = models.ForeignKey('auth.Group')
    active_from = models.DateTimeField(blank=True, null=True)
    active_until = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('directory access group')
        verbose_name_plural = _('directory access groups')
        ordering = ('organization', 'group')
