# encoding: utf-8

from django.core.management import call_command
from django.core.management.base import BaseCommand, make_option


class Command(BaseCommand):
    args = ''
    help = 'Setup all the things'

    option_list = BaseCommand.option_list + (
        make_option('--test',
            action='store_true',
            dest='test',
            default=False,
            help='Setup all the things for testing'
        ),
    )

    def handle(self, *args, **options):
        test = options['test']

        management_commands = (
            (('collectstatic',), dict(interactive=False)),
            (('syncdb',), dict(interactive=False)),
            (('migrate',), dict()),
            (('setup_core',), dict(test=test)),
            (('setup_labour_common_qualifications',), dict(test=test)),
            (('setup_tracon9',), dict(test=test)),
        )

        for pargs, opts in management_commands:
            call_command(*pargs, **opts)
