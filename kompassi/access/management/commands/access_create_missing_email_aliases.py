from sys import stderr

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Create missing email aliases"

    def add_arguments(self, parser):
        parser.add_argument("event_slugs", nargs="+")

    def handle(self, **options):
        from kompassi.core.models import Event

        for event_slug in options["event_slugs"]:
            event = Event.objects.get(slug=event_slug)

            for signup in event.signup_set.all():
                signup.apply_state_email_aliases()
                stderr.write(".")
                stderr.flush()
