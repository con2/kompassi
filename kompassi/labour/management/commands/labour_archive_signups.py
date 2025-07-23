import logging

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction

from kompassi.core.models import Event
from kompassi.labour.models import ArchivedSignup, EmptySignupExtra, LabourEventMeta, Signup

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Archive signups for events"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="+",
            metavar="EVENT_SLUG",
        )

    def handle(self, *args, **options):
        for event_slug in options["event_slugs"]:
            with transaction.atomic():
                logger.info("Archiving signups for event %s...", event_slug)
                event = Event.objects.get(slug=event_slug)
                signups = Signup.objects.filter(event__slug=event_slug)
                SignupExtra = event.labour_event_meta.signup_extra_model

                for signup in signups:
                    ArchivedSignup.archive_signup(signup)

                if SignupExtra:
                    SignupExtra.objects.all().delete()

                signups.delete()

        empty_ctype = ContentType.objects.get_for_model(EmptySignupExtra)
        LabourEventMeta.objects.filter(event__slug__in=options["event_slugs"]).update(
            signup_extra_content_type=empty_ctype
        )
