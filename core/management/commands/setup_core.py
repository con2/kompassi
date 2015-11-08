# encoding: utf-8

from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from ...models import Person


class Command(BaseCommand):
    args = ''
    help = 'Setup core specific stuff'

    def handle(self, *args, **options):
        if settings.DEBUG:
            print "Setting up core in test mode"
            Person.get_or_create_dummy()
        else:
            print "Setting up core in production mode"
