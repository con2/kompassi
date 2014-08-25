from optparse import make_option

from django.core.management.base import BaseCommand, make_option

from core.merge import merge_people
from core.models import Person

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--into',
            action='store',
            type='int',
            dest='into',
        ),
    )

    def handle(*args, **opts):
        people_to_merge = Person.objects.filter(pk__in=[int(i) for i in args])
        person_to_spare = Person.objects.get(pk=opts['into'])
        print 'merging', people_to_merge, 'into', person_to_spare
        merge_people(people_to_merge, into=person_to_spare)