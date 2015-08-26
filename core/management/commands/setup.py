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

        management_commands = [
            (('collectstatic',), dict(interactive=False)),
            (('migrate',), dict()),
            (('setup_core',), dict(test=test)),
            (('setup_labour_common_qualifications',), dict(test=test)),
            (('setup_api_v2',), dict(test=test)),
            (('setup_access',), dict(test=test)),
            (('setup_traconx',), dict(test=test)),
            (('setup_hitpoint2015',), dict(test=test)),
            (('setup_popcultday2015',), dict(test=test)),
            (('setup_yukicon2016',), dict(test=test)),
            (('setup_finncon2016',), dict(test=test)),
        ]

        if test:
            management_commands.extend((
                (('test', 'core', 'labour', 'labour_common_qualifications', 'programme', 'tickets'), dict()),
                (('behave',), dict()),
            ))


        for pargs, opts in management_commands:
            call_command(*pargs, **opts)
