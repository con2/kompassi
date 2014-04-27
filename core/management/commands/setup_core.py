# encoding: utf-8

# Enable johnny-cache for workers etc.
from johnny.cache import enable as enable_johnny_cache
enable_johnny_cache()

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, make_option
from django.contrib.contenttypes.models import ContentType

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
            print "Setting up core in test mode"
            Person.get_or_create_dummy()
        else:
            print "Setting up core in production mode"
