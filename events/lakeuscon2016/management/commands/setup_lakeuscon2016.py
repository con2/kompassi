# encoding: utf-8

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
        self.setup_tickets()
        self.setup_payments()
        self.setup_labour()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Seinäjoen yhteiskoulu', defaults=dict(
            name_inessive='Seinäjoen yhteiskoululla',
        ))
        self.event, unused = Event.objects.get_or_create(slug='lakeuscon2016', defaults=dict(
            name='Lakeuscon',
            name_genitive='Lakeusconin',
            name_illative='Lakeusconiin',
            name_inessive='Lakeusconissa',
            homepage_url='http://www.lakeusconny.fi/',
            organization_name='Lakeuscon NY',
            organization_url='http://www.lakeusconny.fi/',
            start_time=datetime(2016, 5, 7, 10, 0, tzinfo=self.tz),
            end_time=datetime(2016, 5, 7, 20, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2016{:05d}",
            contact_email='Lakeuscon NY <lakeusconny@lakeusconny.fi>',
            ticket_free_text="Tämä on sähköinen lippusi Lakeusconiin. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva Kissakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa Lakeusconhin lauantaina 23. elokuuta 2016 Malmitalolle!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Lakeusconiin!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://www.lakeusconny.fi'>Lakeusconin kotisivuilta</a>.</p>",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            pass

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
                name='Lakeuscon-pääsylippu',
                description='Maksettuasi sinulle lähetetään PDF-lippu antamaasi sähköpostiin, jota vastaan saat rannekkeen tapahtuman ovelta.',
                limit_groups=[
                    limit_group('Pääsyliput', 500),
                ],
                price_cents=700,
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

    def setup_payments(self):
        from payments.models import PaymentsEventMeta
        PaymentsEventMeta.get_or_create_dummy(event=self.event)

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
            work_begins=datetime(2016, 5, 6, 18, 0, tzinfo=self.tz),
            work_ends=datetime(2016, 5, 7, 22, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Lakeuscon NY <lakeusconny@lakeusconny.fi>',
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )
        else:
            # labour_event_meta_defaults.update(
            #     registration_opens=datetime(2015, 1, 22, 0, 0, tzinfo=self.tz),
            #     registration_closes=datetime(2015, 3, 14, 0, 0, tzinfo=self.tz),
            # )
            pass

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            ('Conitea', 'conitea', 'labour'),
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
        conitea = PersonnelClass.objects.get(event=self.event, slug='conitea')
        ohjelma = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        for name, description, pcs in [
            ('Conitea', 'Tapahtuman järjestelytoimikunnan eli Conitean jäsen', [conitea]),
            ('Järjestyksenvalvoja', 'Kävijöiden turvallisuuden valvominen conipaikalla. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi > Pätevyydet).', [tyovoima]),

            # (u'Ohjelmanpitäjä', u'Luennon tai muun vaativan ohjelmanumeron pitäjä', [ohjelma]),
        ]:
            job_category, created = JobCategory.objects.get_or_create(
                event=self.event,
                name=name,
                defaults=dict(
                    description=description,
                    slug=slugify(name),
                )
            )

            if created:
                job_category.personnel_classes = pcs
                job_category.save()

        labour_event_meta.create_groups()

        for slug in ['conitea']:
            JobCategory.objects.filter(event=self.event, slug=slug).update(public=False)

        for jc_name, qualification_name in [
            ('Järjestyksenvalvoja', 'JV-kortti'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

            jc.required_qualifications = [qual]
            jc.save()

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
            slug='conitea',
            defaults=dict(
                title='Conitean ilmoittautumislomake',
                signup_form_class_path='events.lakeuscon2016.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.lakeuscon2016.forms:OrganizerSignupExtraForm',
                active_from=datetime(2015, 8, 18, 0, 0, 0, tzinfo=self.tz),
                active_until=None,
            ),
        )

        for wiki_space, link_title, link_group in [
            # ('LAKEUSWORK', 'Työvoimawiki', 'accepted'),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url='https://confluence.tracon.fi/display/{wiki_space}'.format(wiki_space=wiki_space),
                    group=labour_event_meta.get_group(link_group),
                )
            )


class Command(BaseCommand):
    args = ''
    help = 'Setup lakeuscon2016 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
