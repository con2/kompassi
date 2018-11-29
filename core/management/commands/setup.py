# encoding: utf-8
from django.conf import settings
from django.core.management import call_command, get_commands
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from contextlib import contextmanager


@contextmanager
def noop_context():
    yield


class Command(BaseCommand):
    args = ''
    help = 'Setup all the things'

    def handle(self, *args, **options):
        test = settings.DEBUG

        commands = get_commands()

        organizations = [app_name.split(".")[-1] for app_name in settings.INSTALLED_APPS if app_name.startswith("organizations.")]
        organization_commands = [command for command in ("setup_%s" % organization for organization in organizations) if command in commands]

        events = [app_name.split(".")[-1] for app_name in settings.INSTALLED_APPS if app_name.startswith("events.")]
        event_commands = [command for command in ("setup_%s" % event for event in events) if command in commands]

        management_commands = [
            # (('kompassi_i18n', '-acv2'), dict()),
            # (('collectstatic',), dict(interactive=False)),
            (('migrate',), dict(interactive=False)),
            (('setup_core',), dict()),
            (('setup_labour_common_qualifications',), dict()),
            (('setup_api_v2',), dict()),
            (('setup_access',), dict()),
        ]

        management_commands.extend(((command,), dict()) for command in organization_commands)
        management_commands.extend(((command,), dict()) for command in event_commands)

        management_commands.extend((
            (('setup_listings',), dict()),
            (('access_create_internal_aliases',), dict())
        ))

        for pargs, opts in management_commands:
            print("** Running:", pargs[0])
            with (atomic() if pargs[0].startswith("setup") else noop_context()):
                call_command(*pargs, **opts)
