from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import GroupManagementMixin
from core.utils import get_objects_within_period


class DirectoryOrganizationMeta(models.Model, GroupManagementMixin):
    organization = models.OneToOneField(
        'core.Organization',
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('organization'),
    )

    @property
    def access_groups(self):
        from .directory_access_group import DirectoryAccessGroup
        return get_objects_within_period(
            DirectoryAccessGroup,
            organization=self.organization,
        ).values_list('group', flat=True)

    def is_user_allowed_to_access(self, user):
        return user.is_superuser or user.groups.filter(id__in=self.access_groups)
