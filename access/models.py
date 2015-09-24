# encoding: utf-8

import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import Group

import requests
from requests.exceptions import HTTPError

from core.utils import get_code, SLUG_FIELD_PARAMS
from core.models import Person, Event


logger = logging.getLogger('kompassi')

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


class Privilege(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
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
        verbose_name = u'Myönnetty käyttöoikeus'
        verbose_name_plural = u'Myönnetyt käyttöoikeudet'

        unique_together = [('privilege', 'person')]


class SlackError(RuntimeError):
    pass


class SlackAccess(models.Model):
    privilege = models.OneToOneField(Privilege, related_name='slack_access')
    team_name = models.CharField(max_length=255, verbose_name=u'Slack-yhteisön nimi')
    api_token = models.CharField(max_length=255, default=u'test', verbose_name=u'API-koodi')

    @property
    def invite_url(self):
        return 'https://{team_name}.slack.com/api/users.admin.invite'.format(team_name=self.team_name)

    def grant(self, person):
        if self.api_token == 'test':
            logger.warn(u'Using test mode for SlackAccess Privileges. No invites are actually being sent. '
                u'Would invite {name_and_email} to Slack if an actual API token were set.'.format(
                    name_and_email=person.name_and_email,
                )
            )
            return

        try:
            response = requests.get(self.invite_url, params=dict(
                token=self.api_token,
                email=person.email,
                first_name=person.first_name,
                last_name=person.surname,
                set_active=True,
            ))

            response.raise_for_status()
            result = response.json()

            if not result.get('ok'):
                raise SlackError(result)

            return result
        except (HTTPError, KeyError, IndexError, ValueError) as e:
            unused, unused, trace = sys.exc_info()
            raise SlackError(e), None, trace

    class Meta:
        verbose_name = u'Slack-kutsuautomaatti'
        verbose_name_plural = u'Slack-kutsuautomaatit'
