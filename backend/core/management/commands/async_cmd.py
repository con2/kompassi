from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run an admin command in Celery"

    def add_arguments(self, parser):
        parser.add_argument("async_cmd_args", nargs="+", type=str)

    def handle(self, *args, **options):
        if "background_tasks" not in settings.INSTALLED_APPS:
            raise AssertionError('"background_tasks" not installed')

        from core.tasks import run_admin_command

        run_admin_command.delay(*options["async_cmd_args"])
