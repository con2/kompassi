from sys import stderr

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = '[event_slug...]'
    help = 'Create missing badges for programme'

    def handle(*args, **opts):
        from programme.models import Programme
        from core.models import Event
        from badges.models import Badge

        for event_slug in args[1:]:
            event = Event.objects.get(slug=event_slug)

            for programme in Programme.objects.filter(category__event=event).exclude(state__in=['rejected', 'cancelled']):
                for person in programme.organizers.all():
                    try:
                        Badge.ensure(event=event, person=person)
                        print person
                    except Badge.MultipleObjectsReturned:
                        print u'WARNING: Multiple badges for', person
