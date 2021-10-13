from django.conf import settings
from django.contrib.auth.models import Group

from core.utils import ensure_user_group_membership


def invite_to_slack(privilege, person):
    """
    Invites the user to Slack.

    NOTE: Nowadays done via invite link, so the server-side invite method is noop.
    """
    pass


def add_to_group(privilege, person):
    """
    Generic "add person to group" privilege. The group to add is taken from the privilege slug.
    """

    group = Group.objects.get(name=privilege.slug)
    ensure_user_group_membership(person.user, groups_to_add=[group])
