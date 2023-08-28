from datetime import datetime, timezone, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from programme.models import Programme
from paikkala.models import Program as PaikkalaProgram, Zone as PaikkalaZone
from paikkala.excs import NoCapacity
from core.models import Event
from programme.models.room import Room


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    help = "Block (reserve) all seats in a zone for a programme"

    def add_arguments(self, parser):
        parser.add_argument(
            "--event-slug",
            metavar="EVENT_SLUG",
            required=True,
        )

        parser.add_argument(
            "--programme-title",
            metavar="PROGRAMME_TITLE",
            required=True,
        )

        parser.add_argument(
            "--zone-name",
            nargs="+",
            metavar="ZONE_NAME",
            required=True,
        )

        parser.add_argument(
            "--really",
            default=False,
            action="store_true",
        )

    def handle(*args, **options):
        event = Event.objects.get(slug=options["event_slug"])
        kompassi_programme = Programme.objects.get(title=options["programme_title"], category__event=event)

        with transaction.atomic():
            paikkala_program = PaikkalaProgram.objects.select_for_update().get(
                kompassi_programme=kompassi_programme
            )

            # sudo make the program reservable
            require_contact, require_user, reservation_start, reservation_end = (
                paikkala_program.require_contact,
                paikkala_program.require_user,
                paikkala_program.reservation_start,
                paikkala_program.reservation_end,
            )
            paikkala_program.require_contact = False
            paikkala_program.require_user = False
            paikkala_program.reservation_start = datetime.now(timezone.utc)
            paikkala_program.reservation_end = datetime.now(timezone.utc) + timedelta(days=1)
            paikkala_program.save()

            print(options["zone_name"])
            for zone_name in options["zone_name"]:
                zone = PaikkalaZone.objects.get(room=paikkala_program.room, name=zone_name)
                keep_reserving = True
                while keep_reserving:
                    try:
                        for ticket in paikkala_program.reserve(zone=zone, count=1):
                            print(ticket)
                    except NoCapacity:
                        keep_reserving = False

            paikkala_program.require_contact, paikkala_program.require_user = require_contact, require_user
            paikkala_program.save()

            if not options["really"]:
                raise NotReally("It was only a bad dream :)")
