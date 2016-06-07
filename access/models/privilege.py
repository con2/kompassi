# encoding: utf-8

from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.utils import get_code, SLUG_FIELD_PARAMS
from core.models import Person


class Privilege(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    disclaimers = models.TextField(blank=True)
    request_success_message = models.TextField(blank=True)

    grant_code = models.CharField(max_length=256)

    def grant(self, person):
        gp, created = GrantedPrivilege.objects.get_or_create(
            privilege=self,
            person=person,
            defaults=dict(
                state='approved'
            )
        )

        if gp.state != 'approved':
            return

        if 'background_tasks' in settings.INSTALLED_APPS:
            from .tasks import grant_privilege
            grant_privilege.delay(self.pk, person.pk)
        else:
            self._grant(person)

    def _grant(self, person):
        gp = GrantedPrivilege.objects.get(privilege=self, person=person, state='approved')

        grant_function = get_code(self.grant_code)
        grant_function(self, person)

        gp.state = 'granted'
        gp.save()

    @classmethod
    def get_potential_privileges(cls, person, **extra_criteria):
        assert person.user is not None
        return cls.objects.filter(
            group_privileges__group__in=person.user.groups.all(),
            **extra_criteria
        ).exclude(granted_privileges__person=person).distinct()

    def get_absolute_url(self):
        return u'{base_url}#privilege-{id}'.format(
            base_url=reverse('access_profile_privileges_view'),
            id=self.id,
        )

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('privilege')
        verbose_name_plural = _('privileges')
