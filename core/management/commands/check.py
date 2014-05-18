# encoding: utf-8

from django.core.management import call_command
from django.core.management.base import BaseCommand, make_option


class Command(BaseCommand):
    args = ''
    help = 'Check and fix problems in database integrity'

    option_list = BaseCommand.option_list + (
        make_option('--fix',
            action='store_true',
            dest='test',
            default=False,
            help='Fix problems (default: dry run)'
        ),
    )

    def handle(self, *args, **options):
        test = options['test']

        if args:
            app_labels = set(args)
        else:
            app_labels = None

        from core.checks import autodiscover_checks, run_checks
        autodiscover_checks(app_labels)
        run_checks(app_labels, **options)