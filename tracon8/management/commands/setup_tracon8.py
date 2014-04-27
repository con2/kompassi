# encoding: utf-8

# Enable johnny-cache for workers etc.
from johnny.cache import enable as enable_johnny_cache
enable_johnny_cache()

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, make_option

from dateutil.tz import tzlocal

from core.models import Event, Venue
from programme.models import ProgrammeEventMeta, TimeBlock, SpecialStartTime


class Command(BaseCommand):
    args = ''
    help = 'Setup tracon8 specific stuff'

    option_list = BaseCommand.option_list + (
        make_option('--test',
            action='store_true',
            dest='test',
            default=False,
            help='Set the event up for testing'
        ),
    )

    def handle(*args, **options):
        if options['test']:
            print 'Setting up tracon8 in test mode'
        else:
            print 'Setting up tracon8 in production mode'

        tz = tzlocal()

        venue, unused = Venue.objects.get_or_create(name='Tampere-talo')
        event, unused = Event.objects.get_or_create(slug='tracon8', defaults=dict(
            name='Tracon 8',
            name_genitive='Tracon 8 -tapahtuman',
            name_illative='Tracon 8 -tapahtumaan',
            name_inessive='Tracon 8 -tapahtumassa',
            homepage_url='http://2013.tracon.fi',
            organization_name='Tracon ry',
            organization_url='http://ry.tracon.fi',
            start_time=datetime(2013, 9, 14, 10, 0, tzinfo=tz),
            end_time=datetime(2013, 9, 15, 18, 0, tzinfo=tz),
            venue=venue,
        ))

        admin_group_name = "{installation_name}-{event_slug}-programme-admins".format(
            installation_name=settings.TURSKA_INSTALLATION_SLUG,
            event_slug=event.slug,
        )
        admin_group, unused = Group.objects.get_or_create(name=admin_group_name)
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=event, defaults=dict(
            public=True,
            admin_group=admin_group
        ))

        # v5
        if not programme_event_meta.contact_email:
            programme_event_meta.contact_email = 'ohjelma@tracon.fi'
            programme_event_meta.save()

        # v6
        for start_time, end_time in [
            (
                datetime(2013, 9, 14, 11, 0, 0, tzinfo=tz),
                datetime(2013, 9, 15, 1 , 0, 0, tzinfo=tz)
            ),
            (
                datetime(2013, 9, 15, 9 , 0, 0, tzinfo=tz),
                datetime(2013, 9, 15, 17, 0, 0, tzinfo=tz)
            )
        ]:
            TimeBlock.objects.get_or_create(
                event=event,
                start_time=start_time,
                defaults=dict(
                    end_time=end_time
                )
            )

        SpecialStartTime.objects.get_or_create(
            event=event,
            start_time=datetime(2013, 9, 14, 10, 30, 0, tzinfo=tz),
        )
