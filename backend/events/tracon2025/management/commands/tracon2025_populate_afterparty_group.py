import logging
from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Event
from labour.models import LabourEventMeta

from ...models import SignupExtra

logger = logging.getLogger("kompassi")


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    help = "Populate afterparty privileged & participating groups"

    def add_arguments(self, parser):
        parser.add_argument("--really", default=False, action="store_true")

    def handle(self, *args, **options):
        event = Event.objects.get(slug="tracon2025")

        with transaction.atomic():
            privileged, participating = LabourEventMeta.get_or_create_groups(
                event,
                ["afterparteh", "afterparty"],
            )

            cutoff = date(2025 - 18, 9, 23)

            for sex in SignupExtra.objects.filter(event=event, is_active=True, person__birth_date__lte=cutoff):
                privileged.user_set.add(sex.person.user)
                print(".", end="", flush=True)

            print()
            print(f"privileged: {privileged.user_set.count()} users")

            for sex in SignupExtra.objects.filter(event=event, afterparty_participation=True):
                participating.user_set.add(sex.person.user)  # type: ignore
                print(".", end="", flush=True)

            print()
            print(f"participating: {participating.user_set.count()} users")

            if not options["really"]:
                raise NotReally("It was all a bad dream…")
