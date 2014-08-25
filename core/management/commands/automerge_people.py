from django.core.management.base import BaseCommand, make_option

from core.merge import merge_people, select_person_to_spare
from core.models import Person

class Command(BaseCommand):
    def handle(*args, **opts):
        for email in Person.objects.all().values_list('email', flat=True):
            for people in Person.objects.filter(email=email):
                if people.count() >= 1:
                    for person_to_spare, people_to_merge in possible_merges(people):
                        print 'merging', people_to_merge, 'into', person_to_spare
                        merge_people(people_to_merge, into=person_to_spare)