import sys

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from core.utils import create_temporary_password

from ...utils import ensure_group_exists, create_user, ensure_user_is_member_of_group, CrowdError


def dot(ch="."):
    sys.stdout.write(ch)
    sys.stdout.flush()


class Command(BaseCommand):
    args = ""
    help = "Make sure all users belong to their respective labour groups"

    def handle(*args, **options):
        User = get_user_model()

        for group in Group.objects.all():
            ensure_group_exists(group.name)
            dot()

        for user in User.objects.filter(person__isnull=False):
            try:
                create_user(user, create_temporary_password())
                dot()
            except CrowdError:
                dot("+")

            for group in user.groups.all():
                ensure_user_is_member_of_group(user, group.name)
                dot()
