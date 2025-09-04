import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now
from paikkala.excs import NoCapacity
from paikkala.models.zones import ZoneReservationStatus
from tabulate import tabulate

from kompassi.core.models import Event
from kompassi.program_v2.integrations.paikkala_integration import paikkalize_schedule_item

from ...models.program import Program
from ...models.schedule_item import ScheduleItem

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
        event_slug = options["event_slug"]
        room_slug = options["room_slug"]

        try:
            with transaction.atomic():
                event = Event.objects.get(slug=event_slug)
                meta = event.program_v2_event_meta
                if not meta:
                    raise ValueError("Event is not using Program V2")
                cache = meta.universe.preload_dimensions()

                kompassi_program = Program.objects.create(
                    event=event,
                    title="Paikkala simulation programme",
                )
                kompassi_program.set_dimension_values(dict(room=[room_slug], paikkala=[room_slug]), cache=cache)
                kompassi_program.refresh_cached_fields()

                schedule_item = ScheduleItem(
                    program=kompassi_program,
                    start_time=now(),
                    duration=timedelta(minutes=60),
                    annotations={
                        "paikkala:reservationStartsAt": now().isoformat(),
                    },
                ).with_mandatory_fields()
                schedule_item.save()
                schedule_item.refresh_cached_fields()

                paikkala_program = paikkalize_schedule_item(
                    schedule_item,
                    require_user=False,
                )

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
