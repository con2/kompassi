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
                Programme.objects.filter(category__event=event)
                .exclude(category__slug="aweek-program")
                .select_for_update(of=("self",))
            ):
                content_warnings = [
                    shorten(warn.name)
                    for warn in programme.solmukohta2024_content_warnings.all()
                    if not warn.name.startswith("Other")
                ]
                if programme.content_warnings:
                    content_warnings.append(programme.content_warnings)

                if not content_warnings:
                    continue

                content_warnings_text = ", ".join(content_warnings)
                if content_warnings_text == "None":
                    continue

                content_warnings_text = f"Content warnings: {content_warnings_text}"

                description = programme.description.strip()
                programme.description = f"{description}\n\n{content_warnings_text}"

                if not really:
                    print(programme.description)
                    print("=" * 80)

                bulk_update.append(programme)
            Programme.objects.bulk_update(bulk_update, ["description"])

            if not really:
                raise NotReally("It was only a dream :')")
