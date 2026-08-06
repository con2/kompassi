import logging

from django.core.management.base import BaseCommand

from kompassi.core.models import Event

logger = logging.getLogger(__name__)


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
        for event_slug in options["event_slugs"]:
            event = Event.objects.get(slug=event_slug)
            logger.info("Ensuring badges…", extra=dict(event=event.slug))
            for signup in event.signups.all():
                signup.apply_state_sync()
            logger.info("Ensuring badges done.", extra=dict(event=event.slug))
