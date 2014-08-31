from sys import stderr

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = '[event_slug...]'
    help = 'Create missing badges for labour'

    def handle(*args, **opts):
        from core.models import Event
        for event_slug in args:
            event = Event.objects.get(slug=event_slug)

            for signup in event.signup_set.all():
                signup.ensure_badge_exists_if_necessary()
                stderr.write('.')
                stderr.flush()
