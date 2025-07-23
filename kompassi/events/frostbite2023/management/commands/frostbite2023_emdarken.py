from django.core.management.base import BaseCommand

from kompassi.labour.models.signup import Signup

TITLE_ALLOWLIST = {
    "Pääjärjestäjä",
    "Taltiointivastaava",
    "Tekniikkavastaava",
    "Tiedotus, valokuvaus ja Kompassi",  # that's me!
}

JOB_CATEGORY_ALLOWLIST = {
    "Valokuvaaja",
    "Tekniikka",
    "Taltiointi",
}


class Command(BaseCommand):
    help = "Print a list of people allowed to access the darkroom"

    def handle(self, *args, **options):
        signup_ids = set()

        for signup in Signup.objects.filter(
            event__slug="frostbite2023",
            job_title__in=TITLE_ALLOWLIST,
        ):
            signup_ids.add(signup.id)

        for signup in Signup.objects.filter(
            event__slug="frostbite2023",
            job_categories_accepted__name__in=JOB_CATEGORY_ALLOWLIST,
        ):
            signup_ids.add(signup.id)

        for signup in Signup.objects.filter(id__in=signup_ids).order_by(
            "person__surname",
            "person__firstname",
        ):
            person = signup.person
            if "nick" in person.badge_name_display_style:
                print(f"{person.surname}, {person.first_name}, {person.nick}")
            else:
                print(f"{person.surname}, {person.first_name}")
