from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Create missing badges for programme"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="+",
            metavar="EVENT_SLUG",
        )

    def handle(*args, **opts):
        from programme.models import Programme
        from core.models import Event

        for event_slug in opts["event_slugs"]:
            event = Event.objects.get(slug=event_slug)

            for programme in Programme.objects.filter(category__event=event):
                programme.apply_state()
