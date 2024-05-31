import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Event

from ...importers.graphql import import_graphql
from ...models.program import Program

logger = logging.getLogger("kompassi")


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Import public Program v2 data from another Kompassi installation (eg. production)"

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

        parser.add_argument(
            "--graphql-url",
            default="https://kompassi.eu/graphql",
            help="Base URL of the GraphQL API.",
        )

        parser.add_argument(
            "--language",
            default="fi",
            help="Language of the program data to import.",
        )

    def handle(*args, **opts):
        with transaction.atomic():
            for event_slug in opts["event_slugs"]:
                event = Event.objects.get(slug=event_slug)

                if opts["dangerously_clear"]:
                    Program.objects.filter(event=event).delete()

                import_graphql(event, graphql_url=opts["graphql_url"], language=opts["language"])

            if not opts["really"]:
                raise NotReally("It was only a dream :')")
