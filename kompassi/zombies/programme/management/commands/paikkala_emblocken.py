import logging

from django.core.management.base import BaseCommand
from django.db import transaction
from paikkala.models import PerProgramBlock
from paikkala.models import Program as PaikkalaProgram
from paikkala.models import Zone as PaikkalaZone

from kompassi.core.models import Event
from kompassi.core.utils import log_get_or_create
from kompassi.zombies.programme.models import Programme

logger = logging.getLogger(__name__)


class NotReally(RuntimeError):
    pass


class Command(BaseCommand):
    """
    Example: python manage.py paikkala_emblocken --event-slug tracon2023 --programme-title "AMV-luonnonvoimat" --zone-name "Etuparveke oikea (3. krs)" "Etuparveke vasen (3. krs)" "Takaparveke oikea (3. krs)" "Takaparveke vasen (3. krs)" --really
    """

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
            paikkala_program = PaikkalaProgram.objects.select_for_update(of=("self",), no_key=True).get(
                kompassi_programme=kompassi_programme,
            )

            for zone_name in options["zone_name"]:
                zone = PaikkalaZone.objects.get(room=paikkala_program.room, name=zone_name)
                for row in zone.rows.all():  # type: ignore
                    block, created = PerProgramBlock.objects.get_or_create(
                        program=paikkala_program,
                        row=row,
                        excluded_numbers=f"{row.start_number}-{row.end_number}",
                    )
                    log_get_or_create(logger, block, created)

            if not options["really"]:
                raise NotReally("It was only a bad dream :)")
