import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now
from paikkala.excs import NoCapacity
from paikkala.models.zones import ZoneReservationStatus
from tabulate import tabulate

from kompassi.core.models import Event
from kompassi.zombies.programme.models import Category, Programme, Room

logger = logging.getLogger(__name__)


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    help = "Simulate Paikkala reservations for a room"

    def add_arguments(self, parser):
        parser.add_argument(
            "--event-slug",
            metavar="EVENT_SLUG",
            required=True,
        )

        parser.add_argument(
            "--room-slug",
            metavar="ROOM_SLUG",
            required=True,
        )

    def handle(*args, **options):
        try:
            with transaction.atomic():
                event = Event.objects.get(slug=options["event_slug"])
                room, unused = Room.objects.get_or_create(
                    event=event,
                    slug=options["room_slug"],
                    defaults=dict(
                        name=options["room_slug"],
                    ),
                )
                category = Category.objects.filter(event=event).first()
                kompassi_programme = Programme.objects.create(
                    category=category,
                    title="Paikkala simulation programme",
                    start_time=event.start_time,
                    length=60,
                    room=room,
                    is_using_paikkala=True,
                )

                paikkala_program = kompassi_programme.paikkalize(
                    reservation_start=now(),
                    reservation_end=now() + timedelta(minutes=5),
                    require_user=False,
                )

                assert paikkala_program

                for zone in paikkala_program.zones:
                    print(zone)

                    try:
                        while True:
                            for _reservation in paikkala_program.reserve(zone=zone, count=1):
                                print(".", end="", flush=True)
                    except NoCapacity:
                        pass

                    print()

                results: list[tuple[str, int, int, int]] = []
                for zone in paikkala_program.zones:
                    status: ZoneReservationStatus = zone.get_reservation_status(paikkala_program)
                    results.append((zone.name, status.total_reserved, status.total_remaining, status.total_capacity))

                total_reserved = sum(r[1] for r in results)
                total_remaining = sum(r[2] for r in results)
                total_capacity = sum(r[3] for r in results)

                results.append(("TOTAL", total_reserved, total_remaining, total_capacity))
                print()
                print(tabulate(results, headers=("Zone", "Reserved", "Remaining", "Capacity")))

                if total_reserved != total_capacity:
                    raise AssertionError("All seats must be reserved")
                if total_remaining != 0:
                    raise AssertionError("No seats must be remaining")

                raise NotReally("It was only a dream :)")
        except NotReally:
            pass
