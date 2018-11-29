import logging

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

import requests
from requests.exceptions import HTTPError


logger = logging.getLogger('kompassi')


class SlackError(RuntimeError):
    pass


class SlackAccess(models.Model):
    privilege = models.OneToOneField('access.Privilege', on_delete=models.CASCADE, related_name='slack_access')
    team_name = models.CharField(max_length=255, verbose_name='Slack-yhteisön nimi')
    api_token = models.CharField(max_length=255, default='test', verbose_name='API-koodi')

    @classmethod
    def get_or_create_dummy(cls):
        from .privilege import Privilege
        privilege, unused = Privilege.get_or_create_dummy('slack')

        return cls.objects.get_or_create(
            privilege=privilege,
            defaults=dict(
                team_name='test',
                api_token='x',
            ),
        )

    @property
    def invite_url(self):
        return 'https://{team_name}.slack.com/api/users.admin.invite'.format(team_name=self.team_name)

    def grant(self, person):
        if self.api_token == 'test':
            logger.warn('Using test mode for SlackAccess Privileges. No invites are actually being sent. '
                'Would invite {name_and_email} to Slack if an actual API token were set.'.format(
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
            raise SlackError(e).with_traceback(trace)

    class Meta:
        verbose_name = _('Slack invite automation')
        verbose_name_plural = _('Slack invite automations')
