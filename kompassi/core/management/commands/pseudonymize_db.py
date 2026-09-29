from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = (
        "Pseudonymize all personal data and delete all secrets in the database. "
        "Refuses to run unless the database name contains 'pseudo'."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--really",
            action="store_true",
            help="Confirm that you want to pseudonymize this database.",
        )
        parser.add_argument(
            "--check",
            action="store_true",
            help="List fields that may hold personal data but are neither pseudonymized nor reviewed as safe.",
        )

    def handle(self, *args, **options):
        from kompassi.core.pseudonymization import find_stale_classifications, find_unclassified_fields, pseudonymize

        if options["check"]:
            problems = find_unclassified_fields() + [f"{name} (stale)" for name in find_stale_classifications()]
            for problem in problems:
                self.stdout.write(problem)
            if problems:
                raise CommandError(f"{len(problems)} fields need a rule or an entry in NOT_PERSONAL")
            return

        database_name = settings.DATABASES["default"]["NAME"]
        if "pseudo" not in database_name:
            raise CommandError(f"Database name {database_name!r} does not contain 'pseudo'.")
        if not options["really"]:
            raise CommandError(f"Pass --really to confirm you want to pseudonymize {database_name!r}.")

        with transaction.atomic():
            for model_label, summary in pseudonymize():
                self.stdout.write(f"{model_label}: {summary}")

        self.stdout.write(self.style.SUCCESS("Pseudonymization complete."))
