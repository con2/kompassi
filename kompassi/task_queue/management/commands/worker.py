from django.core.management.base import BaseCommand

from ...worker import Worker


class Command(BaseCommand):
    help = "Run background tasks enqueued via django.tasks."

    def add_arguments(self, parser):
        parser.add_argument(
            "--once",
            default=False,
            action="store_true",
            help="Run all currently ready tasks and then exit.",
        )

    def handle(self, *args, **opts):
        worker = Worker()
        if opts["once"]:
            worker.run_until_empty()
        else:
            worker.run_forever()
