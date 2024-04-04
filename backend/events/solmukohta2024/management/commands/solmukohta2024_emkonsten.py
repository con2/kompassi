from django.core.management.base import BaseCommand
from django.db import transaction

from core.models.event import Event
from programme.models.programme import Programme


class NotReally(RuntimeError):
    pass


def shorten(warning: str):
    return warning.split("(", 1)[0].strip()


class Command(BaseCommand):
    help = "Add content warnings to the end of programme descriptions."

    def add_arguments(self, parser):
        parser.add_argument("--really", default=False, action="store_true")

    def handle(self, *args, **options):
        really = options["really"]

        with transaction.atomic():
            event = Event.objects.get(slug="solmukohta2024")

            bulk_update = []
            for programme in (
                Programme.objects.filter(
                    category__event=event,
                    tags__slug="sk-advance-signup",
                    signup_link="",
                )
                .exclude(category__slug="aweek-program")
                .select_for_update(of=("self",))
            ):
                programme.signup_link = f"https://konsti.solmukohta.eu/games/p{programme.id}"

                if not really:
                    print(programme.title)
                    print(programme.signup_link)
                    print()

                bulk_update.append(programme)
            Programme.objects.bulk_update(bulk_update, ["signup_link"])

            if not really:
                raise NotReally("It was only a dream :')")
