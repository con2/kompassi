from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from core.models import GroupManagementMixin, Person
from core.utils import get_objects_within_period


class DirectoryOrganizationMeta(models.Model, GroupManagementMixin):
    organization = models.OneToOneField(
        'core.Organization',
        primary_key=True,
        verbose_name=_('organization'),
    )

    @property
    def access_groups(self):
        from .directory_access_group import DirectoryAccessGroup
        return get_objects_within_period(
            DirectoryAccessGroup,
            organization=self,
        ).values_list('group', flat=True)

    def is_user_allowed_to_access(self, user):
        return user.is_superuser or user.groups.filter(id__in=self.access_groups)

    @property
    def people(self):
        """
        Returns people with badges in events of the current organization
        """
        # have signups
        q = Q(signups__event__organization=self.organization)

        # or programmes
        q |= Q(programme_roles__programme__category__event__organization=self.organization)

        # or are members
        q |= Q(memberships__organization=self.organization)

        return Person.objects.filter(q).distinct()
