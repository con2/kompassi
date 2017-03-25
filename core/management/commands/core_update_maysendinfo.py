# encoding: utf-8



import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User


logger = logging.getLogger("kompassi")


class Command(BaseCommand):
    args = ''
    help = 'Update group of users that may receive info mail'

    def handle(self, *args, **options):
        group = Group.objects.get(name=settings.KOMPASSI_MAY_SEND_INFO_GROUP_NAME)
        users = User.objects.filter(person__may_send_info=True)
        result = group.user_set.set(users, clear=True)
        logger.info("{num_users} users will now receive info spam".format(
            num_users=Group.objects.get(
                name=settings.KOMPASSI_MAY_SEND_INFO_GROUP_NAME
            ).user_set.count(),
        ))
