# encoding: utf-8

from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.utils import slugify


class Setup(object):
    def __init__(self):
        self._ordering = 0

    def get_ordering_number(self):
        self._ordering += 10
        return self._ordering

    def setup(self, test=False):
        self.test = test
        self.tz = tzlocal()
        self.setup_core()
        self.setup_labour()
        # self.setup_programme()

    def setup_core(self):
        from core.models import Organization, Venue, Event

        self.organization, unused = Organization.objects.get_or_create(slug='kawacon-ry', defaults=dict(
            name='Kawacon ry',
            homepage_url='http://www.kawacon.info',
        ))
        self.venue, unused = Venue.objects.get_or_create(name='Joensuun normaalikoulu', defaults=dict(
            name_inessive='Joensuun normaalikoululla' # XXX not really inessive
        ))
        self.event, unused = Event.objects.get_or_create(slug='kawacon2017', defaults=dict(
            name='Kawacon (2017)',
            name_genitive='Kawaconin',
            name_illative='Kawaconiin',
            name_inessive='Kawaconissa',
            homepage_url='http://www.kawacon.info',
            organization=self.organization,
            start_time=datetime(2017, 7, 1, 10, 0, tzinfo=self.tz),
            end_time=datetime(2017, 7, 2, 18, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_labour(self):
        from core.models import Person, Event
        from labour.models import (
            AlternativeSignupForm,
            InfoLink,
            Job,
            JobCategory,
            LabourEventMeta,
            Perk,
            PersonnelClass,
            Qualification,
            WorkPeriod,
        )
        from ...models import SpecialDiet, SignupExtra, Night, Shift
        from django.contrib.contenttypes.models import ContentType

        labour_admin_group, = LabourEventMeta.get_or_create_groups(self.event, ['admins'])

        if self.test:
            from core.models import Person
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2017, 6, 30, 8, 0, tzinfo=self.tz),
            work_ends=datetime(2017, 7, 3, 16, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Kawacon <henna.merilain@gmail.com>',
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )
        else:
            pass

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            (u'Conitea', 'conitea', 'labour'),
            (u'Vänkäri', 'tyovoima', 'labour'),
            (u'Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
            (u'Myyjä', 'myyja', 'badges'),
            (u'Vieras', 'vieras', 'badges'),
        ]:
            personnel_class, created = PersonnelClass.objects.get_or_create(
                event=self.event,
                slug=pc_slug,
                defaults=dict(
                    name=pc_name,
                    app_label=pc_app_label,
                    priority=self.get_ordering_number(),
                ),
            )

        if not JobCategory.objects.filter(event=self.event).exists():
            JobCategory.copy_from_event(
                source_event=Event.objects.get(slug='kawacon2016'),
                target_event=self.event
            )

        labour_event_meta.create_groups()

        for diet_name in [
            u'Gluteeniton',
            u'Laktoositon',
            u'Maidoton',
            u'Vegaaninen',
            u'Lakto-ovo-vegetaristinen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        for night in [
            u'Perjantain ja lauantain välinen yö',
            u'Lauantain ja sunnuntain välinen yö',
            u'Sunnuntain ja maanantain välinen yö',
        ]:
            Night.objects.get_or_create(name=night)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug=u'conitea',
            defaults=dict(
                title=u'Conitean ilmoittautumislomake',
                signup_form_class_path='events.kawacon2017.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.kawacon2017.forms:OrganizerSignupExtraForm',
                active_from=datetime(2017, 3, 15, 0, 0, 0, tzinfo=self.tz),
                active_until=self.event.end_time,
            ),
        )

        for shift_name in [
            'Perjantaina',
            'Lauantaina',
            'Sunnuntaina',
            'Sunnuntai-iltana ja maanantaina',
        ]:
            Shift.objects.get_or_create(name=shift_name)        

    def setup_programme(self):
        from programme.models import Room, ProgrammeEventMeta, Category, TimeBlock, View, SpecialStartTime
        from core.utils import full_hours_between

        room_order = 0
        for room_name in [
            # u'Auditorio',
            # u'Pääsali',
            # u'E-rakennus, luokat',
            # u'Kawaplay, G-rakennus',
            # u'Elokuvateatteri Tapio',
        ]:
            room_order += 100
            Room.objects.get_or_create(
                venue=self.venue,
                name=room_name,
                defaults=dict(
                    order=room_order,
                )
            )

        admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ['admins', 'hosts'])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            admin_group=admin_group,
        ))

        view, unused = View.objects.get_or_create(
            event=self.event,
            name='Ohjelmakartta',
        )

        if not view.rooms.exists():
            view.rooms = Room.objects.filter(venue=self.venue, active=True)
            view.save()

        for category_name, category_style in [
            # (u'Luento', u'anime'),
            # (u'Non-stop', u'miitti'),
            (u'Työpaja', u'rope'),
            (u'Muu ohjelma', u'muu'),
            # (u'Show', u'cosplay'),
        ]:
            Category.objects.get_or_create(
                event=self.event,
                title=category_name,
                defaults=dict(
                    style=category_style,
                )
            )

        for start_time, end_time in [
            (
                self.event.start_time,
                self.event.start_time.replace(hour=18),
            ),
            (
                self.event.end_time.replace(hour=10),
                self.event.end_time,
            ),
        ]:
            TimeBlock.objects.get_or_create(
                event=self.event,
                start_time=start_time,
                defaults=dict(
                    end_time=end_time
                )
            )

            # <Kharnis> Lisäksi, saapiko ohjelmakartan toimimaan 30 min tarkkuudella?
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(start_time, end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(
                    event=self.event,
                    start_time=hour_start_time.replace(minute=30)
                )


class Command(BaseCommand):
    args = ''
    help = 'Setup kawacon2017 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
