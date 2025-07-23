from django.core.management.base import BaseCommand

from kompassi.core.merge_people import merge_people, possible_merges
from kompassi.core.models import Person


class Command(BaseCommand):
    def handle(*args, **opts):
        for email in Person.objects.all().values_list("email", flat=True).distinct():
            if not email:
                continue

            people = Person.objects.filter(email=email)
            if people.count() > 1:
                print(email)
                for person_to_spare, people_to_merge in possible_merges(people):
                    merge_people(people_to_merge, into=person_to_spare)
