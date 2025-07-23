import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from kompassi.core.models import Event
from kompassi.core.utils import log_get_or_create
from kompassi.zombies.tickets.models import AccommodationInformation, LimitGroup

from ...models import Night, SignupExtra

logger = logging.getLogger(__name__)


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    help = "Creates accommodees from signups"

    def add_arguments(self, parser):
        parser.add_argument("--really", default=False, action="store_true")

    def handle(self, *args, **options):
        with transaction.atomic():
            event = Event.objects.get(slug="tracon2025")

            for night in Night.objects.all():
                limit_group, created = LimitGroup.objects.get_or_create(
                    event=event,
                    limit=0,
                    description=f"Työvoimamajoitus {night}",
                )

                log_get_or_create(logger, limit_group, created)

                for sex in SignupExtra.objects.filter(
                    event=event,
                    is_active=True,
                    lodging_needs=night,
                ):
                    person = sex.person

                    # cannot use AccommodationInformation due to m2m
                    # I know, it really sucks for full namesakes :()
                    accom = AccommodationInformation.objects.filter(
                        limit_groups=limit_group,
                        first_name=person.first_name,
                        last_name=person.surname,
                    ).first()

                    if accom:
                        log_get_or_create(logger, accom, False)
                    else:
                        accom = AccommodationInformation.objects.create(
                            first_name=person.first_name,
                            last_name=person.surname,
                            phone_number=person.normalized_phone_number,
                            email=person.email,
                        )
                        accom.limit_groups.set([limit_group])
                        log_get_or_create(logger, accom, True)

            if not options["really"]:
                raise NotReally("It was only a bad dream :)")
