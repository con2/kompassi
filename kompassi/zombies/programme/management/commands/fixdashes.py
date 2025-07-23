from django.core.management.base import BaseCommand

from kompassi.zombies.programme.models import Programme


class Command(BaseCommand):
    args = ""
    help = "Fix dashes in programme descriptions"

    def handle(*args, **options):
        for programme in Programme.objects.all():
            if " - " in programme.title or " - " in programme.description:
                programme.title = programme.title.replace(" - ", " – ")
                programme.description = programme.description.replace(" - ", " – ")
                programme.save()
