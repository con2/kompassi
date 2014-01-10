# encoding: utf-8

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, make_option
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import get_default_timezone, now

from ...models import Person

class Command(BaseCommand):
    args = ''
    help = 'Setup core specific stuff'

    option_list = BaseCommand.option_list + (
        make_option('--test',
            action='store_true',
            dest='test',
            default=False,
            help='Set the core up for testing'
        ),
    )

    def handle(self, *args, **options):
        if options['test']:
            Person.create_dummy()