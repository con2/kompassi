from django.core.management.base import BaseCommand

from core.models.event import Event
from program_v2.utils.backfill import backfill


class Command(BaseCommand):
    help = """
    Backfill program_v2 dimensions and involvement.
    Use this if the logic for dimensions changes while there is already data for the event.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--override-involvement-dimensions",
            action="store_true",
            default=False,
            help="Override involvement dimensions for given events",
        )
        parser.add_argument("event_slugs", nargs="+", help="Event slugs to backfill")

    def handle(self, *args, **options):
        for event_slug in options["event_slugs"]:
            event = Event.objects.get(slug=event_slug)
            backfill(event, override_involvement_dimensions=options["override_involvement_dimensions"])
