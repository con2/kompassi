# encoding: utf-8

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import Group

from core.utils import get_code, SLUG_FIELD_PARAMS
from core.models import Person, Event


class Privilege(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    request_success_message = models.TextField(blank=True)

    grant_code = models.CharField(max_length=256)

    def grant(self, person):
        if 'background_tasks' in settings.INSTALLED_APPS:
            from .tasks import grant_privilege
            grant_privilege.delay(self.pk, person.pk)
        else:
            self._grant(person)

    def _grant(self, person):
        # Won't use get_or_create because we want to make sure privilege granting succeeds before
        # recording the privilege as granted.

        try:
            return GrantedPrivilege.objects.get(privilege=self, person=person)
        except GrantedPrivilege.DoesNotExist:
            grant_function = get_code(self.grant_code)
            grant_function(self, person)

            return GrantedPrivilege.objects.create(privilege=self, person=person)

    @classmethod
    def get_potential_privileges(cls, person, **extra_criteria):
        assert person.user is not None
        return cls.objects.filter(
            group_privileges__group__in=person.user.groups.all(),
            **extra_criteria
        ).exclude(granted_privileges__person=person)

    def get_absolute_url(self):
        return u'{base_url}#privilege-{id}'.format(
            base_url=reverse('access_profile_privileges_view'),
            id=self.id,
        )

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Käyttöoikeus'
        verbose_name_plural = u'Käyttöoikeudet'


class GroupPrivilege(models.Model):
    privilege = models.ForeignKey(Privilege, related_name='group_privileges')
    group = models.ForeignKey(Group, related_name='group_privileges')
    event = models.ForeignKey(Event, null=True, blank=True, related_name='group_privileges')

    def __unicode__(self):
        return u'{group_name} - {privilege_title}'.format(
            group_name=self.group.name if self.group else None,
            privilege_title=self.privilege.title if self.privilege else None,
        )

    class Meta:
        verbose_name = u'Ryhmän käyttöoikeus'
        verbose_name_plural = u'Ryhmien käyttöoikeudet'

        unique_together = [('privilege', 'group')]


class GrantedPrivilege(models.Model):
    privilege = models.ForeignKey(Privilege, related_name='granted_privileges')
    person = models.ForeignKey(Person, related_name='granted_privileges')

    granted_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'{person_name} - {privilege_title}'.format(
            person_name=self.person.full_name if self.person else None,
            privilege_title=self.privilege.title if self.privilege else None,
        )

    class Meta:
        verbose_name = u'Myönnetty käyttöoikeus'
        verbose_name_plural = u'Myönnetyt käyttöoikeudet'

        unique_together = [('privilege', 'person')]
