# encoding: utf-8

import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from ...models import Person
from ...utils import log_get_or_create


logger = logging.getLogger("kompassi")


class Command(BaseCommand):
    args = ''
    help = 'Setup core specific stuff'

    def handle(self, *args, **options):
        if settings.DEBUG:
            person, created = Person.get_or_create_dummy()
            log_get_or_create(logger, person, created)
        else:
            print("Setting up core in production mode")

        for group_name in settings.KOMPASSI_NEW_USER_GROUPS:
            group, created = Group.objects.get_or_create(name=group_name)
            log_get_or_create(logger, group, created)

        group, created = Group.objects.get_or_create(name=settings.KOMPASSI_MAY_SEND_INFO_GROUP_NAME)
        log_get_or_create(logger, group, created)
