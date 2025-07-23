import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from kompassi.core.models import Event
from kompassi.labour.models import LabourEventMeta

from ...models import SignupExtra

logger = logging.getLogger(__name__)


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    help = "Creates accommodees from signups"

    def add_arguments(self, parser):
        parser.add_argument("--really", default=False, action="store_true")

    def handle(self, *args, **options):
        event = Event.objects.get(slug="tracon2022")

        with transaction.atomic():
            (group,) = LabourEventMeta.get_or_create_groups(event, ["afterparty"])

            for sex in SignupExtra.objects.filter(event=event, afterparty_participation=True):
                group.user_set.add(sex.person.user)  # type: ignore
                print(".", end="", flush=True)

            print()

            if not options["really"]:
                raise NotReally("It was all a bad dream…")
