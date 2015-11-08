from django.conf import settings

from core.utils import ensure_user_group_membership

from .models import SlackAccess



def invite_to_slack(privilege, person):
    """
    Invites the user to Slack.
    """
    privilege.slack_access.grant(person)


def add_to_group(privilege, person):
    """
    Generic "add person to group" privilege. The group to add is taken from the privilege slug.
    """

    group = Group.objects.get(name=privilege.slug)
    ensure_user_group_membership(person.user, groups_to_add=[group])
