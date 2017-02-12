# encoding: utf-8

from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.utils import full_hours_between


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
        self.setup_programme()
        self.setup_access()
        self.setup_badges()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Lahden Sibeliustalo', defaults=dict(
            name_inessive='Lahden Sibeliustalolla',  # not really inessive though
        ))
        self.event, unused = Event.objects.get_or_create(slug='desucon2017', defaults=dict(
            name='Desucon (2017)',
            name_genitive='Desuconin',
            name_illative='Desuconiin',
            name_inessive='Desuconissa',
            homepage_url='https://desucon.fi/desucon2017/',
            organization_name='Kehittyvien conien Suomi ry',
            organization_url='https://desucon.fi/kcs/',
            start_time=datetime(2017, 6, 16, 17, 0, 0, tzinfo=self.tz),
            end_time=datetime(2017, 6, 18, 17, 0, 0, tzinfo=self.tz),
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
        from ...models import SignupExtra, SpecialDiet
        from django.contrib.contenttypes.models import ContentType

        labour_admin_group, = LabourEventMeta.get_or_create_groups(self.event, ['admins'])

        if self.test:
            from core.models import Person
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2017, 6, 16, 8, 0, tzinfo=self.tz),
            work_ends=datetime(2017, 6, 18, 21, 0, tzinfo=self.tz),
            registration_opens=datetime(2017, 1, 12, 18, 0, tzinfo=self.tz),
            registration_closes=datetime(2017, 2, 19, 23, 59, 59, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Desuconin työvoimavastaava <tyovoima@desucon.fi>',
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            ('Vastaava', 'vastaava', 'labour'),
            ('Vuorovastaava', 'vuorovastaava', 'labour'),
            ('Työvoima', 'tyovoima', 'labour'),
            ('Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
            ('Guest of Honour', 'goh', 'programme'),
            ('Media', 'media', 'badges'),
            ('Myyjä', 'myyja', 'badges'),
            ('Vieras', 'vieras', 'badges'),
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
                source_event=Event.objects.get(slug='desucon2016'),
                target_event=self.event
            )

        labour_event_meta.create_groups()

        organizer_form, unused = AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug='vastaava',
            defaults=dict(
                title='Vastaavan ilmoittautumislomake',
                signup_form_class_path='events.desucon2017.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.desucon2017.forms:OrganizerSignupExtraForm',
                active_from=datetime(2017, 1, 22, 0, 0, 0, tzinfo=self.tz),
                active_until=self.event.start_time,
            ),
        )

        if organizer_form.active_until is None:
            organizer_form.active_until = self.event.start_time
            organizer_form.save()

        for diet_name in [
            'Gluteeniton',
            'Laktoositon',
            'Maidoton',
            'Vegaaninen',
            'Lakto-ovo-vegetaristinen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug='xxlomake',
            defaults=dict(
                title='Erikoistehtävien ilmoittautumislomake',
                signup_form_class_path='events.desucon2017.forms:SpecialistSignupForm',
                signup_extra_form_class_path='events.desucon2017.forms:SpecialistSignupExtraForm',
                active_from=datetime(2017, 1, 22, 0, 0, 0, tzinfo=self.tz),
                active_until=self.event.start_time,
                signup_message=(
                    'Täytä tämä lomake vain, '
                    'jos joku Desuconin vastaavista on ohjeistanut sinun ilmoittautua tällä lomakkeella. '
                ),
            ),
        )

    def setup_badges(self):
        from badges.models import BadgesEventMeta

        badge_admin_group, = BadgesEventMeta.get_or_create_groups(self.event, ['admins'])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                badge_layout='trad',
                real_name_must_be_visible=True,
            )
        )

    def setup_programme(self):
        from labour.models import PersonnelClass
        from programme.models import (
            AlternativeProgrammeForm,
            Category,
            ProgrammeEventMeta,
            Role,
            Room,
            SpecialStartTime,
            TimeBlock,
            View,
        )

        ProgrammeEventMeta.get_or_create_groups(self.event, ['hosts'])
        programme_admin_group, = ProgrammeEventMeta.get_or_create_groups(self.event, ['admins'])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            public=False,
            admin_group=programme_admin_group,
            contact_email='Desuconin ohjelmavastaava <ohjelma@desucon.fi>',
        ))

        personnel_class = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        room_order = 0
        for room_name in [
            'Pääsali',
            'Kuusi',
            'Puuseppä',
            'Koivu',
            'Honka',
        ]:
            Room.objects.get_or_create(
                venue=self.event.venue,
                name=room_name,
                defaults=dict(
                    order=room_order,
                ),
            )
            room_order += 10

        role_priority = 0
        for role_title in [
            'Ohjelmanjärjestäjä',
            'Panelisti',
            'Työpajanpitäjä',
            'Keskustelupiirin vetäjä',
        ]:
            role, unused = Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=True,
                    require_contact_info=True,
                    priority=role_priority,
                )
            )
            role_priority += 10

        for title, slug, style in [
            ('Muu ohjelma', 'other', 'color1'),
            ('Paneeli', 'paneeli', 'color2'),
            ('Luento', 'luento', 'color3'),
            ('Keskustelupiiri', 'keskustelupiiri', 'color4'),
            ('Paja', 'paja', 'color5'),
            ('Pienluento', 'pienluento', 'color6'),
            ('Esitys', 'esit', 'color7'),
            ('Visa', 'visa', 'color7'),
            ('Erikoisohjelma', 'erik', 'color7'),
            ('Sisäinen ohjelma', 'sisainen-ohjelma', 'sisainen'),
        ]:
            Category.objects.get_or_create(
                event=self.event,
                slug=slug,
                defaults=dict(
                    title=title,
                    style=style,
                    public=style != 'sisainen',
                )
            )

        form, created = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug='default',
            defaults=dict(
                title='Ohjelmalomake',
                short_description='',
                programme_form_code='events.desucon2017.forms:ProgrammeForm',
                active_from=datetime(2017, 1, 22, 0, 0, 0, tzinfo=self.tz),
                num_extra_invites=0,
            )
        )

        if not TimeBlock.objects.filter(event=self.event).exists():
            for start_time, end_time in [
                (
                    datetime(2017, 6, 16, 17, 0, 0, tzinfo=self.tz),
                    datetime(2017, 6, 17, 1, 0, 0, tzinfo=self.tz),
                ),
                (
                    datetime(2017, 6, 17, 9, 0, 0, tzinfo=self.tz),
                    datetime(2017, 6, 18, 1, 0, 0, tzinfo=self.tz),
                ),
                (
                    datetime(2017, 6, 18, 9, 0, 0, tzinfo=self.tz),
                    datetime(2017, 6, 18, 18, 0, 0, tzinfo=self.tz),
                ),
            ]:
                TimeBlock.objects.get_or_create(
                    event=self.event,
                    start_time=start_time,
                    defaults=dict(
                        end_time=end_time
                    )
                )

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(
                    event=self.event,
                    start_time=hour_start_time.replace(minute=30)  # look, no tz
                )

        view, created = View.objects.get_or_create(
            event=self.event,
            name='Ohjelmakartta',
        )
        if created:
            view.rooms = self.event.venue.room_set.all()
            view.save()

    def setup_access(self):
        from access.models import Privilege, GroupPrivilege

        # Grant accepted workers and programme hosts access to Desucon Slack
        privilege = Privilege.objects.get(slug='desuslack')
        for group in [
            self.event.labour_event_meta.get_group('accepted'),
            self.event.programme_event_meta.get_group('hosts'),
        ]:
            GroupPrivilege.objects.get_or_create(group=group, privilege=privilege, defaults=dict(event=self.event))


class Command(BaseCommand):
    args = ''
    help = 'Setup desucon2017 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
