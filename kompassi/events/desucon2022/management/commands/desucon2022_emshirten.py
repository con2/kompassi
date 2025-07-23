from django.core.management.base import BaseCommand

from kompassi.badges.models import Badge
from kompassi.core.models import Event
from kompassi.labour.models.signup import Signup

from ...models import SignupExtra

TITLE_MAPPING = {
    "Ohjelmanjärjestäjä": "STAFF",
    "Näkymätön ohjelmanjärjestäjä": "NO_SHIRT",
    "Panelisti": "NO_SHIRT",
    "Työpajanpitäjä": "NO_SHIRT",
    "Keskustelupiirin vetäjä": "NO_SHIRT",
    "Tuomari": "NO_SHIRT",
    "Tiedotus, valokuvaus ja Kompassi": "KUVAAJA",  # that's me!
    "Yövastaava": "DESURITY",
    "DesuTv Lead": "DESUTV",
    "Turvallisuusvastaava": "DESURITY",
    "Turvallisuusvastaava II": "DESURITY",
}

JOB_CATEGORY_MAPPING = {
    "DesuTV": "DESUTV",
    "Järjestyksenvalvoja": "DESURITY",
    "Valokuvaaja": "KUVAAJA",
    # "Taltiointi": "KUVAAJA",
}


class Command(BaseCommand):
    help = "Sort people into their respective houses of STAFF, KUVAAJA and NO_SHIRT"

    def add_arguments(self, parser):
        parser.add_argument("--really", default=False, action="store_true")

    def handle(self, *args, **options):
        really = options["really"]
        signup_extras = SignupExtra.objects.filter(is_active=True)
        event = Event.objects.get(slug="desucon2022")

        for signup_extra in signup_extras:
            person = signup_extra.person
            shirt_type = "STAFF"
            method = "DEFAULT"

            try:
                signup = Signup.objects.get(event=event, person=person)
            except Signup.DoesNotExist:
                pass
            else:
                for jc_name, jc_shirt_type in JOB_CATEGORY_MAPPING.items():
                    if signup.job_categories_accepted.filter(name=jc_name).exists():
                        shirt_type = jc_shirt_type
                        method = "JOB_CAT"

            try:
                badge = Badge.objects.get(personnel_class__event=event, person=signup_extra.person)
            except Badge.DoesNotExist:
                pass
            else:
                if bad_shirt_type := TITLE_MAPPING.get(badge.job_title):
                    shirt_type = bad_shirt_type
                    method = "TITLE"

            if signup_extra.shirt_type != shirt_type:
                print(method, shirt_type, signup_extra.person.full_name, sep="\t")

                if really:
                    signup_extra.shirt_type = shirt_type
                    signup_extra.save()
