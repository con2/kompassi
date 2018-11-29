import logging

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now


logger = logging.getLogger('kompassi')


class GroupEmailAliasGrant(models.Model):
    group = models.ForeignKey('auth.Group', on_delete=models.CASCADE, verbose_name='Ryhmä')
    type = models.ForeignKey('access.EmailAliasType', on_delete=models.CASCADE, verbose_name='Tyyppi')
    active_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{group_name}: {type}'.format(
            group_name=self.group.name if self.group else None,
            type=self.type,
        )

    @classmethod
    def ensure_aliases(cls, person, t=None):
        if person.user is None:
            logger.warn('Cannot ensure_aliases for Person without User: %s', person.full_name)
            return

        if t is None:
            t = now()

        group_grants = cls.objects.filter(group__in=person.user.groups.all())

        # filter out inactive grants
        group_grants = group_grants.filter(Q(active_until__gt=t) | Q(active_until__isnull=True))

        for group_grant in group_grants:
            group_grant.type.create_alias_for_person(person, group_grant=group_grant)

    def admin_get_organization(self):
        return self.type.domain.organization
    admin_get_organization.short_description = _('organization')
    admin_get_organization.admin_order_field = 'type__domain__organization'

    class Meta:
        verbose_name = _('group e-mail alias grant')
        verbose_name_plural = ('group e-mail alias grants')
