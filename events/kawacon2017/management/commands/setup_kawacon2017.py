# encoding: utf-8

from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal


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
        self.setup_tickets()
        self.setup_payments()

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
            ('Conitea', 'conitea', 'labour'),
            ('Vänkäri', 'tyovoima', 'labour'),
            ('Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
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
                source_event=Event.objects.get(slug='kawacon2016'),
                target_event=self.event
            )

        labour_event_meta.create_groups()

        for diet_name in [
            'Gluteeniton',
            'Laktoositon',
            'Maidoton',
            'Vegaaninen',
            'Lakto-ovo-vegetaristinen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        for night in [
            'Perjantain ja lauantain välinen yö',
            'Lauantain ja sunnuntain välinen yö',
            'Sunnuntain ja maanantain välinen yö',
        ]:
            Night.objects.get_or_create(name=night)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug='conitea',
            defaults=dict(
                title='Conitean ilmoittautumislomake',
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
            ('Työpaja', 'rope'),
            ('Muu ohjelma', 'muu'),
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

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=120,
            reference_number_template="2017{:05d}",
            contact_email='Kawacon -lipunmyynti <kawacon.myynti@gmail.comi>',
            ticket_free_text=(
                "Tämä on sähköinen lippusi Kawaconiin. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva Kissakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa Kawaconiin!"
            ),
            front_page_text=(
                "<h2>Tervetuloa ostamaan pääsylippuja Kawacon 2017 -tapahtumaan!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://kawacon.info'>Kawaconin kotisivuilta</a>.</p>"
            ),
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            defaults.update(
                ticket_sales_starts=datetime(2017, 3, 31, 0, 0, 0, tzinfo=self.tz),
                ticket_sales_ends=datetime(2017, 6, 30, 23, 59, 59, tzinfo=self.tz),
            )

        meta, unused = TicketsEventMeta.objects.get_or_create(event=self.event, defaults=defaults)

        def limit_group(description, limit):
            limit_group, unused = LimitGroup.objects.get_or_create(
                event=self.event,
                description=description,
                defaults=dict(limit=limit),
            )

            return limit_group

        for product_info in [
            dict(
                name='Viikonloppulippu',
                description=(
                    'Viikonloppulippu Kawacon 2017 -tapahtumaan. Voimassa koko viikonlopun '
                    'ajan. Toimitetaan sähköpostitse PDF-tiedostona, jossa olevaa viivakoodia '
                    'vastaan saat rannekkeen tapahtumaan saapuessasi.'
                ),
                limit_groups=[
                    limit_group('Pääsyliput', 10000),
                ],
                price_cents=1300,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
        ]:
            name = product_info.pop('name')
            limit_groups = product_info.pop('limit_groups')

            product, unused = Product.objects.get_or_create(
                event=self.event,
                name=name,
                defaults=product_info
            )

            if not product.limit_groups.exists():
                product.limit_groups = limit_groups
                product.save()

    def setup_payments(self):
        from payments.models import PaymentsEventMeta
        PaymentsEventMeta.get_or_create_dummy(event=self.event)

class Command(BaseCommand):
    args = ''
    help = 'Setup kawacon2017 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
