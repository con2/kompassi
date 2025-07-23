import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from kompassi.zombies.programme.models.programme import Programme
from kompassi.zombies.programme.models.special_reservation import SpecialReservation

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            for programme in Programme.objects.filter(
                category__event__slug="tracon2024",
                room__slug="pieni-sali",
                is_using_paikkala=True,
            ):
                paikkala_program = programme.paikkala_program
                if not paikkala_program:
                    raise ValueError(f"Programme {programme} has no Paikkala program")

                reservation, created = SpecialReservation.objects.get_or_create(
                    program=paikkala_program,
                    defaults=dict(
                        zone=paikkala_program.zones.filter(name="Permanto vasen (2. krs)").first(),
                        row_name="1",
                        description="Aukku tietää",
                    ),
                )

                print(f"https://kompassi.eu{reservation.get_absolute_url()}", reservation.program)
