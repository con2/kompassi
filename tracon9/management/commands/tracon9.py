# encoding: utf-8

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, make_option
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import get_default_timezone, now

from core.models import Event, Venue
from labour.models import EventMeta
from ...models import SignupExtra

class Command(BaseCommand):
    args = ''
    help = 'Setup tracon9 specific stuff'

    option_list = BaseCommand.option_list + (
        make_option('--test',
            action='store_true',
            dest='test',
            default=False,
            help='Set the event up for testing'
        ),
    )

    def handle(*args, **options):
        venue, unused = Venue.objects.get_or_create(name="Tampere-talo")
        content_type = ContentType.objects.get_for_model(SignupExtra)
        event, unused = Event.objects.get_or_create(slug="tracon9", defaults=dict(
            name="Tracon 9",
            venue=venue
        ))

        tz = get_default_timezone()

        if options['test']:
            t = now()
            event_meta_defaults = dict(
                signup_extra_content_type=content_type,
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60)
            )
        else:
            event_meta_defaults = dict(
                signup_extra_content_type=content_type,
                registration_opens=datetime(2014, 3, 1, 0, 0, tzinfo=tz),
                registration_closes=datetime(2014, 8, 1, 0, 0, tzinfo=tz)
            )

        event_meta, unused = EventMeta.objects.get_or_create(event=event, defaults=event_meta_defaults)