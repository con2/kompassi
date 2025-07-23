from sys import stderr

from django.core.management.base import BaseCommand
from django.db import transaction

from ...models.badge import Badge


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Refresh perks (eg. upon perk logic change)"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="+",
            metavar="EVENT_SLUG",
        )

        parser.add_argument("--really", default=False, action="store_true")

    def handle(self, *args, **options):
        from kompassi.core.models import Event

        really = options["really"]

        with transaction.atomic():
            for event_slug in options["event_slugs"]:
                event = Event.objects.get(slug=event_slug)
                stderr.write(event.slug + "\n")

                for badge in Badge.objects.filter(
                    personnel_class__event=event,
                ).select_for_update(of=("self",), no_key=True):
                    _, updated = badge.reemperkelate()
                    stderr.write("+" if updated else ".")
                    stderr.flush()

                stderr.write("\n")

            if not really:
                raise NotReally("It was only a dream :')")
