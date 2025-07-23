import json
from sys import stdin

from django.core.management.base import BaseCommand
from django.db import transaction

from kompassi.badges.models import Badge
from kompassi.core.models import Event
from kompassi.labour.models.personnel_class import PersonnelClass

from .solmukohta2020_extract import Participant


class Command(BaseCommand):
    args = ""
    help = "Extract solmukohta2020 participants from google sheets"

    def add_arguments(self, parser):
        parser.add_argument("--really", default=False, action="store_true")

    def handle(self, *args, **options):
        really = options["really"]
        event = Event.objects.get(slug="ropecon2022")
        personnel_class = PersonnelClass.objects.get(event=event, name="Vapaalippu")
        signup_data = json.load(stdin)

        with transaction.atomic():
            for ptp_dict in signup_data:
                ptp = Participant(**ptp_dict)

                # Match email
                if Badge.objects.filter(
                    personnel_class__event=event,
                    person__email=ptp.email,
                ).exists():
                    print("EXIST_EMAIL", ptp, sep="\t")
                    continue

                # Match first name and surname
                if Badge.objects.filter(
                    personnel_class__event=event,
                    first_name=ptp.first_name,
                    surname=ptp.surname,
                ).exists():
                    print("EXIST_NAME", ptp, sep="\t")
                    continue

                # Match neither, create one
                badge = Badge(
                    personnel_class=personnel_class,
                    first_name=ptp.first_name,
                    surname=ptp.surname,
                    job_title="Solmukohta 2020",
                )

                if really:
                    badge.save()
                    print("BADGE_CREATED", ptp, sep="\t")
                else:
                    print("WOULD_CREATE", ptp, sep="\t")
