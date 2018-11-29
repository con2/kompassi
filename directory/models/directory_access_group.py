from django.db import models
from django.utils.translation import ugettext_lazy as _


class DirectoryAccessGroup(models.Model):
    """
    Grants expiring group access to the personnel directory.
    """

    organization = models.ForeignKey('core.Organization', on_delete=models.CASCADE)
    group = models.ForeignKey('auth.Group', on_delete=models.CASCADE)
    active_from = models.DateTimeField(blank=True, null=True)
    active_until = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('directory access group')
        verbose_name_plural = _('directory access groups')
        ordering = ('organization', 'group')
