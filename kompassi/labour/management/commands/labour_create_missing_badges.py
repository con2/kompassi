from sys import stderr

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Create missing badges for labour"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="+",
            metavar="EVENT_SLUG",
        )

    def handle(self, *args, **options):
        from kompassi.core.models import Event

        for event_slug in options["event_slugs"]:
            event = Event.objects.get(slug=event_slug)

            for signup in event.signup_set.all():
                signup.apply_state_create_badges()
                stderr.write(".")
                stderr.flush()
