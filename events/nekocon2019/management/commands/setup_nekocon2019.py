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
        self.setup_labour()
        # self.setup_tickets()
        # self.setup_payments()
        self.setup_programme()

    def setup_core(self):
        from core.models import Venue, Event, Organization

        self.venue, unused = Venue.objects.get_or_create(name='Kuopion musiikkikeskus', defaults=dict(
            name_inessive='Kuopion musiikkikeskuksessa',
        ))
        self.organization, unused = Organization.objects.get_or_create(
            slug='nekocon-ry',
            defaults=dict(
                name='Nekocon ry',
                homepage_url='https://nekocon.fi',
            )
        )
        self.event, unused = Event.objects.get_or_create(slug='nekocon2019', defaults=dict(
            name='Nekocon (2019)',
            name_genitive='Nekoconin',
            name_illative='Nekoconiin',
            name_inessive='Nekoconissa',
            homepage_url='https://nekocon.fi',
            organization=self.organization,
            start_time=datetime(2019, 7, 13, 10, 00, tzinfo=self.tz),
            end_time=datetime(2019, 7, 14, 17, 0, tzinfo=self.tz),
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
        from ...models import SignupExtra, SpecialDiet, Night
        from django.contrib.contenttypes.models import ContentType

        labour_admin_group, = LabourEventMeta.get_or_create_groups(self.event, ['admins'])

        if self.test:
            from core.models import Person
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2015, 7, 12, 12, 0, tzinfo=self.tz),
            work_ends=datetime(2015, 7, 14, 22, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Nekoconin työvoimatiimi <tyovoima@nekocon.fi>',
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
            ('Conitea', 'conitea', 'labour'),
            ('Työvoima', 'tyovoima', 'labour'),
            ('Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
            ('Kunniavieras', 'goh', 'programme'),
            ('Media', 'media', 'badges'),
            ('Myyjä', 'myyja', 'badges'),
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

        for name, description, pcs in [
            ('Conitea', 'Tapahtuman järjestelytoimikunnan eli conitean jäsen', [conitea]),
            ('Järjestyksenvalvoja', 'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).', [tyovoima]),
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
                job_category.personnel_classes.set(pcs)


        labour_event_meta.create_groups()

        for name in ['Conitea']:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ('Järjestyksenvalvoja', 'JV-kortti'),
            # (u'Green room', u'Hygieniapassi'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

        period_length = timedelta(hours=8)
        for period_description, period_start in [
            ("Perjantain kasaus (pe klo 12–21)", None),
            ("Lauantain aamuvuoro (la klo 08–14)", None),
            ("Lauantain iltapäivävuoro (la klo 14–20)", None),
            ("Lauantain iltavuoro (la klo 20–02)", None),
            ("Lauantai–sunnuntai-yövuoro (su klo 02–08)", None),
            ("Sunnuntain aamuvuoro (su klo 08–14)", None),
            ("Sunnuntain iltapäivävuoro ja purku (su klo 14–20)", None),
        ]:
            WorkPeriod.objects.get_or_create(
                event=self.event,
                description=period_description,
                defaults=dict(
                    start_time=period_start,
                    end_time=(period_start + period_length) if period_start else None,
                )
            )

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
        ]:
            Night.objects.get_or_create(name=night)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug='conitea',
            defaults=dict(
                title='Conitean ilmoittautumislomake',
                signup_form_class_path='events.nekocon2019.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.nekocon2019.forms:OrganizerSignupExtraForm',
                active_from=datetime(2018, 11, 13, 18, 0, 0, tzinfo=self.tz),
                active_until=datetime(2019, 7, 14, 23, 59, 59, tzinfo=self.tz),
            ),
        )

        for wiki_space, link_title, link_group in [
            ('NEKOCON2019', 'Coniteawiki', 'conitea'),
            # ('NEKOWORK', 'Työvoimawiki', 'accepted'),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url='https://confluence.tracon.fi/display/{wiki_space}'.format(wiki_space=wiki_space),
                    group=labour_event_meta.get_group(link_group),
                )
            )

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=120,
            reference_number_template="2015{:05d}",
            contact_email='Nekocon (2019) <liput@nekocon.fi>',
            ticket_free_text="Tämä on sähköinen lippusi Nekocon (2019) -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva Kissakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa Nekocon (2019) -tapahtumaan!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Nekocon (2019) -tapahtumaan!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://2015.nekocon.fi'>Nekocon (2019) -tapahtuman kotisivuilta</a>.</p>"
                "<p>Huom! Tämä verkkokauppa palvelee ainoastaan asiakkaita, joilla on osoite Suomessa. Mikäli tarvitset "
                "toimituksen ulkomaille, ole hyvä ja ota sähköpostitse yhteyttä: <em>liput@nekocon.fi</em>"
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
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
            # dict(
            #     name='Nekocon (2019) -pääsylippu',
            #     description='Viikonloppuranneke Kuopiossa järjestettävään Animecon-tapahtumaan. Huom. myynnissä vain viikonloppurannekkeita. Lippu lähetetään postitse.',
            #     limit_groups=[
            #         limit_group('Pääsyliput', 3000),
            #     ],
            #     price_cents=1600,
            #     requires_shipping=True,
            #     electronic_ticket=False,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name='Lattiamajoituspaikka (koko vkl)',
            #     description='Lattiamajoituspaikka molemmiksi öiksi pe-la ja la-su. Majoituksesta lisää tietoa sivuillamme www.nekocon.fi.',
            #     limit_groups=[
            #         limit_group('Lattiamajoitus pe-la', 445),
            #         limit_group('Lattiamajoitus la-su', 445),
            #     ],
            #     price_cents=1000,
            #     requires_shipping=False,
            #     electronic_ticket=False,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name='Lattiamajoituspaikka (pe-la)',
            #     description='Lattiamajoituspaikka perjantain ja lauantain väliseksi yöksi. Majoituksesta lisää tietoa sivuillamme www.nekocon.fi.',
            #     limit_groups=[
            #         limit_group('Lattiamajoitus pe-la', 445),
            #     ],
            #     price_cents=700,
            #     requires_shipping=False,
            #     electronic_ticket=False,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name='Lattiamajoituspaikka (la-su)',
            #     description='Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi. Majoituksesta lisää tietoa sivuillamme www.nekocon.fi.',
            #     limit_groups=[
            #         limit_group('Lattiamajoitus la-su', 445),
            #     ],
            #     price_cents=700,
            #     requires_shipping=False,
            #     electronic_ticket=False,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
            # dict(
            #     name='Nekocon (2019) -konserttilippu',
            #     description='Lippu Nekoconin konserttiin. Mikäli tarvitset pyörätuolipaikkaa, otathan ennen ostoa yhteyttä <em>liput@nekocon.fi</em>, jotta voimme varmistaa paikkatilanteen.',
            #     limit_groups=[
            #         limit_group('Konserttiliput', 820),
            #     ],
            #     price_cents=500,
            #     requires_shipping=True,
            #     electronic_ticket=False,
            #     available=True,
            #     ordering=self.get_ordering_number(),
            # ),
        ]:
            name = product_info.pop('name')
            limit_groups = product_info.pop('limit_groups')

            product, unused = Product.objects.get_or_create(
                event=self.event,
                name=name,
                defaults=product_info
            )

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)
                product.save()

    def setup_payments(self):
        from payments.models import PaymentsEventMeta
        PaymentsEventMeta.get_or_create_dummy(event=self.event)

    def setup_programme(self):
        from core.utils import full_hours_between
        from labour.models import PersonnelClass
        from programme.models import (
            Category,
            Programme,
            ProgrammeEventMeta,
            Role,
            Room,
            SpecialStartTime,
            TimeBlock,
            View,
        )

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ['admins', 'hosts'])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            public=False,
            admin_group=programme_admin_group,
            contact_email='Nekoconin ohjelmatiimi <ohjelma@nekocon.fi>',
        ))

        personnel_class = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        role, unused = Role.objects.get_or_create(
            personnel_class=personnel_class,
            title='Ohjelmanjärjestäjä',
            defaults=dict(
                is_default=True,
                require_contact_info=True,
            )
        )

        have_categories = Category.objects.filter(event=self.event).exists()
        if not have_categories:
            for title, style in [
                ('Anime ja manga', 'anime'),
                ('Cosplay', 'cosplay'),
                ('Paja', 'miitti'),
                ('Muu ohjelma', 'muu'),
                ('Kunniavieras', 'rope'),
            ]:
                Category.objects.get_or_create(
                    event=self.event,
                    style=style,
                    defaults=dict(
                        title=title,
                    )
                )

        for start_time, end_time in [
            (
                self.event.start_time.replace(hour=10, minute=0),
                self.event.start_time.replace(hour=20, minute=0),
            ),
            (
                self.event.end_time.replace(hour=10, minute=0),
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

        SpecialStartTime.objects.get_or_create(
            event=self.event,
            start_time=self.event.start_time,
        )

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(
                    event=self.event,
                    start_time=hour_start_time.replace(minute=30)
                )


class Command(BaseCommand):
    args = ''
    help = 'Setup nekocon2019 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
