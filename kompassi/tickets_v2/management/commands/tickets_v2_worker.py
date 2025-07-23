import logging

from django.core.management.base import BaseCommand

from ...worker import run, tick

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "A worker that sends receipts."

    def add_arguments(self, parser):
        parser.add_argument(
            "--once",
            default=False,
            action="store_true",
            help="Only run once and then exit.",
        )

    def handle(*args, **opts):
        if opts["once"]:
            while tick():
                pass
        else:
            run()
