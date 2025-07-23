import logging

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ""
    help = "Update group of users that may receive info mail"

    def handle(self, *args, **options):
        group = Group.objects.get(name=settings.KOMPASSI_MAY_SEND_INFO_GROUP_NAME)
        users = User.objects.filter(person__may_send_info=True)
        group.user_set.set(users, clear=True)
        logger.info(
            "%d users will now receive info spam",
            Group.objects.get(name=settings.KOMPASSI_MAY_SEND_INFO_GROUP_NAME).user_set.count(),
        )
