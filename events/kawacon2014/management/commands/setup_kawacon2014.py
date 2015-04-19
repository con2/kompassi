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
            help='Setup kawacon for testing'
        ),
    )

    def handle(*args, **options):
        if options['test']:
            print 'Setting up kawacon2014 in test mode'
        else:
            print 'Setting up kawacon2014 in production mode'

        tz = tzlocal()

        venue, unused = Venue.objects.get_or_create(name='Peltolan ammattiopisto', defaults=dict(
            name_inessive='Peltolan ammattiopistolla' # XXX not really inessive
        ))

        room_order = 0
        for room_name in [
            u'Auditorio',
            u'Pääsali',
            u'E-rakennus, luokat',
            u'Kawaplay, G-rakennus',
            u'Elokuvateatteri Tapio',
        ]:
            room_order += 100
            Room.objects.get_or_create(
                venue=venue,
                name=room_name,
                defaults=dict(
                    order=room_order,
                )
            )

        event, unused = Event.objects.get_or_create(slug='kawacon2014', defaults=dict(
            name='Kawacon 2014',
            name_genitive='Kawacon 2014 -tapahtuman',
            name_illative='Kawacon 2014 -tapahtumaan',
            name_inessive='Kawacon 2014 -tapahtumassa',
            homepage_url='http://kawacon.info',
            organization_name='Kawacon ry',
            organization_url='http://kawacon.info',
            start_time=datetime(2014, 6, 28, 10, 0, tzinfo=tz),
            end_time=datetime(2014, 6, 29, 18, 0, tzinfo=tz),
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
            (u'Non-stop', u'miitti'),
            (u'Työpaja', u'rope'),
            (u'Muu ohjelma', u'muu'),
            (u'Show', u'cosplay'),
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
                datetime(2014, 6, 28, 10, 0, 0, tzinfo=tz),
                datetime(2014, 6, 28, 18, 0, 0, tzinfo=tz),
            ),
            (
                datetime(2014, 6, 29, 10, 0, 0, tzinfo=tz),
                datetime(2014, 6, 29, 16, 0, 0, tzinfo=tz),
            ),
        ]:
            TimeBlock.objects.get_or_create(
                event=event,
                start_time=start_time,
                defaults=dict(
                    end_time=end_time
                )
            )
