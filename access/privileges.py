from django.conf import settings

import requests
from requests.exceptions import HTTPError

from core.utils import ensure_user_is_member_of_group


class SlackError(RuntimeError):
    pass


def invite_to_slack(privilege, person):
    """
    Invites the user to Slack.
    """

    if not settings.KOMPASSI_ACCESS_SLACK_API_TOKEN:
        print u'NOTE: Would invite {name_and_email} to Slack'.format(name_and_email=person.name_and_email)
        print u'To actually invite, set settings.KOMPASSI_ACCESS_SLACK_API_TOKEN.'
        print
        return

    try:
        response = requests.get(settings.KOMPASSI_ACCESS_SLACK_INVITE_URL, params=dict(
            token=settings.KOMPASSI_ACCESS_SLACK_API_TOKEN,
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


def add_to_group(privilege, person):
    """
    Generic "add person to group" privilege. The group to add is taken from the privilege slug.
    """

    group = Group.objects.get(name=privilege.slug)
    ensure_user_is_member_of_group(person.user, group)
