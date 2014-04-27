# encoding: utf-8

from datetime import datetime

from django.core.management.base import BaseCommand, make_option

from dateutil.tz import tzlocal

from core.models import Venue, Event
from programme.models import ProgrammeEventMeta, Category, Room, TimeBlock, View


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--test',
            action='store_true',
            dest='test',
            default=False,
            help='Setup concon9 for testing'
        ),
    )

    def handle(*args, **options):
        if options['test']:
            print 'Setting up concon9 in test mode'
        else:
            print 'Setting up concon9 in production mode'

        tz = tzlocal()

        venue, unused = Venue.objects.get_or_create(
            name=u'Metropolia AMK Hämeentie',
            defaults=dict(
                name_inessive=u'Metropolia AMK:n Hämeentien toimipisteessä'
            )
        )

        room_order = 0
        for room_name in [
            u'Track 1',
            u'Track 2',
        ]:
            room_order += 100
            Room.objects.get_or_create(
                venue=venue,
                name=room_name,
                defaults=dict(
                    order=room_order,
                )
            )

        event, unused = Event.objects.get_or_create(slug='concon9', defaults=dict(
            name='Concon 9',
            name_genitive='Concon 9 -seminaarin',
            name_illative='Concon 9 -seminaariin',
            name_inessive='Concon 9 -seminaarissa',
            homepage_url='http://concon.nakkikone.org',
            organization_name='Yliopiston anime ja manga ry',
            organization_url='http://yama.animeunioni.org',
            start_time=datetime(2014, 5, 24, 10, 0, tzinfo=tz),
            end_time=datetime(2014, 5, 24, 18, 0, tzinfo=tz),
            venue=venue,
        ))

        admin_group, unused = ProgrammeEventMeta.get_or_create_group(event=event, suffix='admins')
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=event, defaults=dict(
            public=False,
            admin_group=admin_group,
        ))

        view, unused = View.objects.get_or_create(
            event=event,
            name='Ohjelmakartta',
        )

        view.rooms = Room.objects.filter(venue=venue, public=True)
        view.save()

        for category_name, category_style in [
            (u'Luento', u'anime'),
            (u'Keskustelu', u'miitti'),
            (u'Työpaja', u'rope'),
            (u'Muu ohjelma', u'muu'),
        ]:
            Category.objects.get_or_create(
                event=event,
                title=category_name,
                defaults=dict(
                    style=category_style,
                )
            )

        for start_time, end_time in [
            (
                event.start_time,
                event.end_time,
            ),
        ]:
            TimeBlock.objects.get_or_create(
                event=event,
                start_time=start_time,
                defaults=dict(
                    end_time=end_time
                )
            )
