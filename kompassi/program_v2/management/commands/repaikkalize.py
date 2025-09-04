from django.core.management.base import BaseCommand
from django.db import transaction

from kompassi.core.models import Event

from ...integrations.paikkala_integration import repaikkalize_event


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Create missing badges for programme"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="+",
            metavar="EVENT_SLUG",
        )

        parser.add_argument(
            "--really",
            default=False,
            action="store_true",
        )

    @transaction.atomic
    def handle(*args, **opts):
        for event_slug in opts["event_slugs"]:
            event = Event.objects.get(slug=event_slug)
            repaikkalize_event(event)

            if not opts["really"]:
                raise NotReally("It was all a bad dream :)")
