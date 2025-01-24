from django.core.management.base import BaseCommand

from badges.models import Badge
from core.models import Event
from labour.models.signup import Signup

from ...models import SignupExtra

TITLE_MAPPING = {
    "Ohjelmanjärjestäjä": "STAFF",
    "Näkymätön ohjelmanjärjestäjä": "NO_SHIRT",
    "Panelisti": "NO_SHIRT",
    "Työpajanpitäjä": "NO_SHIRT",
    "Keskustelupiirin vetäjä": "NO_SHIRT",
    "Tuomari": "NO_SHIRT",
    "Valokuvausvastaava": "KUVAAJA",  # that's me!
    "Kompassi": "KUVAAJA",  # that's me hopefully in the future!
    "Yövastaava": "DESURITY",
    "Manager of Desurity": "DESURITY",
    "DesuTv Lead": "DESUTV",
    "DesuTV Vastaava": "DESUTV",
    "Turvallisuusvastaava": "DESURITY",
    "Turvallisuussuunnittelu": "DESURITY",
}

JOB_CATEGORY_MAPPING = {
    "DesuTV": "DESUTV",
    "Järjestyksenvalvoja": "DESURITY",
    "Valokuvaus": "KUVAAJA",
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
        event = Event.objects.get(slug="frostbite2025")

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
            except (Badge.DoesNotExist, Badge.MultipleObjectsReturned):
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
