import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Event

from ...models import Program

logger = logging.getLogger("kompassi")


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Import program v1 data to v2"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="+",
            metavar="EVENT_SLUG",
        )

        parser.add_argument(
            "--really",
            action="store_true",
            default=False,
        )

        parser.add_argument(
            "--dangerously-clear",
            action="store_true",
            default=False,
            help="Clear all existing program data before importing.",
        )

    def handle(*args, **opts):
        with transaction.atomic():
            for event_slug in opts["event_slugs"]:
                event = Event.objects.get(slug=event_slug)
                Program.import_program_v1(event, clear=opts["dangerously_clear"])

            if not opts["really"]:
                raise NotReally("It was only a dream :')")
