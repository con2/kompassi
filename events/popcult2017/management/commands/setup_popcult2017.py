# encoding: utf-8

from __future__ import unicode_literals

import os
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.utils import slugify


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', *parts))


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
        self.setup_badges()
        self.setup_tickets()
        self.setup_payments()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Scandic Marina Congress Center', defaults=dict(
            name_inessive='Scandic Marina Congress Centerissä',
        ))
        self.event, unused = Event.objects.get_or_create(slug='popcult2017', defaults=dict(
            name='Popcult Helsinki 2017',
            name_genitive='Popcult Helsinki 2017 -tapahtuman',
            name_illative='Popcult Helsinki 2017 -tapahtumaan',
            name_inessive='Popcult Helsinki 2017 -tapahtumassa',
            homepage_url='http://popcult.fi/helsinki-2017',
            organization_name='Finnish Fandom Conventions ry',
            organization_url='http://popcult.fi',
            start_time=datetime(2017, 5, 6, 10, 0, tzinfo=self.tz),
            end_time=datetime(2017, 5, 7, 18, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_labour(self):
        from core.models import Person
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
        from ...models import SignupExtra
        from django.contrib.contenttypes.models import ContentType

        labour_admin_group, = LabourEventMeta.get_or_create_groups(self.event, ['admins'])

        if self.test:
            from core.models import Person
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time - timedelta(days=1),
            work_ends=self.event.end_time + timedelta(hours=4),
            admin_group=labour_admin_group,
            contact_email='Popcult Helsingin työvoimavastaava <virve.honkala@popcult.fi>',
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
            ('Työvoima', 'tyovoima', 'labour'),
            ('Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
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

        tyovoima = PersonnelClass.objects.get(event=self.event, slug='tyovoima')
        vastaava = PersonnelClass.objects.get(event=self.event, slug='vastaava')

        for jc_data in [
            (
                'Vastaava',
                'Tapahtuman järjestelytoimikunnan jäsen eli vastaava',
                [vastaava]
            ),
            (
                'Järjestyksenvalvoja',
                'Järjestyksenvalvojan tehtäviin kuuluvat lippujen tarkistus, kulunvalvonta sekä ihmisten ohjaus. Tehtävään vaaditaan JV-kortti.',
                [tyovoima]
            ),
        ]:
            if len(jc_data) == 3:
                name, description, pcs = jc_data
                job_names = []
            elif len(jc_data) == 4:
                name, description, pcs, job_names = jc_data
            else:
                raise ValueError("Length of jc_data must be 3 or 4")

            job_category, created = JobCategory.objects.get_or_create(
                event=self.event,
                slug=slugify(name),
                defaults=dict(
                    name=name,
                    description=description,
                )
            )

            if created:
                job_category.personnel_classes = pcs
                job_category.save()

            for job_name in job_names:
                job, created = Job.objects.get_or_create(
                    job_category=job_category,
                    slug=slugify(job_name),
                    defaults=dict(
                        title=job_name,
                    )
                )

        labour_event_meta.create_groups()

        JobCategory.objects.filter(event=self.event, slug='vastaava').update(public=False)

        for jc_name, qualification_name in [
            ('Järjestyksenvalvoja', 'JV-kortti'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)
            if not jc.required_qualifications.exists():
                jc.required_qualifications = [qual]
                jc.save()

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug='vastaava',
            defaults=dict(
                title='Vastaavien ilmoittautumislomake',
                signup_form_class_path='events.popcult2017.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.popcult2017.forms:OrganizerSignupExtraForm',
                active_from=datetime(2017, 1, 12, 0, 0, 0, tzinfo=self.tz),
                active_until=self.event.start_time,
            ),
        )

    def setup_badges(self):
        from badges.models import BadgesEventMeta

        badge_admin_group, = BadgesEventMeta.get_or_create_groups(self.event, ['admins'])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                badge_layout='nick',
            )
        )        

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2017{:05d}",
            contact_email='Popcult Helsinki <liput@popcult.fi>',
            plain_contact_email='liput@popcult.fi',
            ticket_free_text=
                "Tämä on sähköinen lippusi Popcult Helsinki 2017 -tapahtumaan. Sähköinen lippu vaihdetaan\n"
                "rannekkeeseen lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai\n"
                "näyttää sen älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole\n"
                "mahdollista, ota ylös kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva\n"
                "Kissakoodi ja ilmoita se lipunvaihtopisteessä.\n\n"
                "Tervetuloa Popcult Helsinkiin!",
            front_page_text=u"<h2>Tervetuloa ostamaan pääsylippuja Popcult Helsinki 2017 -tapahtumaan!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://popcult.fi/helsinki-2017'>Popcult Helsinki 2017 -tapahtuman kotisivuilta</a>.</p>",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            defaults.update(
                ticket_sales_starts=datetime(2016, 12, 5, 18, 0, tzinfo=self.tz),
                # ticket_sales_ends=datetime(2015, 1, 11, 18, 0, tzinfo=self.tz),
            )

        meta, unused = TicketsEventMeta.objects.get_or_create(event=self.event, defaults=defaults)

        def limit_group(description, limit):
            limit_group, unused = LimitGroup.objects.get_or_create(
                event=self.event,
                description=description,
                defaults=dict(limit=limit),
            )

            return limit_group

        def ordering():
            ordering.counter += 10
            return ordering.counter
        ordering.counter = 0

        for product_info in [
            dict(
                name='Popcult Helsinki 2017 -pääsylippu',
                description='Lippu kattaa koko viikonlopun. Maksettuasi sinulle lähetetään PDF-lippu antamaasi sähköpostiin, jota vastaan saat rannekkeen tapahtuman ovelta.',
                limit_groups=[
                    limit_group('Pääsyliput', 2000),
                ],
                price_cents=2600,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
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

        # v5
        if not meta.print_logo_path:
            meta.print_logo_path = mkpath('static', 'images', 'popcult.png')
            meta.print_logo_width_mm = 30
            meta.print_logo_height_mm = 30
            meta.save()

    def setup_payments(self):
        from payments.models import PaymentsEventMeta
        PaymentsEventMeta.get_or_create_dummy(event=self.event)


class Command(BaseCommand):
    args = ''
    help = 'Setup popcult2017 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
