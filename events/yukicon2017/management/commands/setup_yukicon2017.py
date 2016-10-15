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
        self.setup_tickets()
        self.setup_payments()
        self.setup_labour()
        self.setup_programme()
        self.setup_badges()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Messukeskuksen Kokoustamo', defaults=dict(
            name_inessive='Messukeskuksen Kokoustamossa',
        ))
        self.event, unused = Event.objects.get_or_create(slug='yukicon2017', defaults=dict(
            name='Yukicon 4.0 & Pyrycon',
            name_genitive='Yukicon 4.0 -tapahtuman',
            name_illative='Yukicon 4.0 -tapahtumaan',
            name_inessive='Yukicon 4.0 -tapahtumassa',
            homepage_url='http://www.yukicon.fi',
            organization_name='Yukitea ry',
            organization_url='http://www.yukicon.fi',
            start_time=datetime(2017, 2, 18, 10, 0, tzinfo=self.tz),
            end_time=datetime(2017, 2, 19, 18, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2017{:05d}",
            contact_email='Yukicon <yukicon@yukicon.fi>',
            plain_contact_email='yukicon@yukicon.fi',
            ticket_free_text="Tämä on sähköinen lippusi. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa tapahtumaan!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Yukicon 4.0- ja Pyrycon-tapahtumiin!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://www.yukicon.fi' target='_blank'>Yukiconin kotisivuilta</a>.</p>",
            print_logo_path=mkpath('static', 'images', 'yukicon2017_logo.png'),
            print_logo_width_mm=50,
            print_logo_height_mm=16
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )

        meta, unused = TicketsEventMeta.objects.get_or_create(event=self.event, defaults=defaults)

        if 'yukicon_436_test' in meta.print_logo_path:
            meta.print_logo_path = mkpath('static', 'images', 'yukicon2017_logo.png')
            meta.print_logo_height_mm = 16
            meta.save()

        def limit_group(description, limit):
            limit_group, unused = LimitGroup.objects.get_or_create(
                event=self.event,
                description=description,
                defaults=dict(limit=limit),
            )

            return limit_group

        for product_info in [
            dict(
                name='Yukicon 4.0 – Early Access',
                description='Early Access -lipulla pääset Yukiconiin 18.–19.2.2017. Lippu oikeuttaa Early Access -etuuksien lunastuksen. Lippu ei oikeuta pääsyä Pyryconiin. Maksettuasi sinulle lähetetään PDF-lippu antamaasi sähköpostiin, jota vastaan saat rannekkeen tapahtuman ovelta.',
                limit_groups=[
                    limit_group('Early Access', 200),
                ],
                price_cents=2900,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Pyryconin pääsylippu',
                description='Lipulla pääset Pyryconiin perjantaina 17. helmikuuta 2017. Lippu ei oikeuta pääsyä Yukiconiin. Maksettuasi sinulle lähetetään PDF-lippu antamaasi sähköpostiin, jota vastaan saat rannekkeen tapahtuman ovelta. Ei palautus- tai vaihto-oikeutta.',
                limit_groups=[
                    limit_group('Pyrycon', 1200),
                ],
                price_cents=600,
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

    def setup_programme(self):
        from labour.models import PersonnelClass
        from programme.models import (
            Category,
            Programme,
            ProgrammeEventMeta,
            Role,
            Room,
            SpecialStartTime,
            Tag,
            TimeBlock,
            View,
        )
        from core.utils import full_hours_between

        for room_name in [
            '207',
            '208',
            '209',
            'Pelihuone',
            'Iso sali',
        ]:
            Room.objects.get_or_create(
                venue=self.venue,
                name=room_name,
                defaults=dict(
                    order=self.get_ordering_number(),
                )
            )

        admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ['admins', 'hosts'])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            admin_group=admin_group,
        ))

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        for pc_slug, role_title, role_is_default in [
            ('ohjelma', 'Ohjelmanjärjestäjä', True),
        ]:
            personnel_class = PersonnelClass.objects.get(event=self.event, slug=pc_slug)
            role, unused = Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_is_default,
                )
            )

        view, unused = View.objects.get_or_create(
            event=self.event,
            name='Ohjelmakartta',
        )

        if not view.rooms.exists():
            view.rooms = Room.objects.filter(venue=self.venue, active=True)
            view.save()

        for category_name, category_style in [
            ('Pelit', 'rope'),
            ('Anime/manga', 'anime'),
            ('Cosplay', 'cosplay'),
            ('Muu', 'muu'),
        ]:
            Category.objects.get_or_create(
                event=self.event,
                title=category_name,
                defaults=dict(
                    style=category_style,
                )
            )

        for tag_name, tag_style in [
            ('Luento', 'label-default'),
            ('Paneeli', 'label-success'),
            ('Keskustelupiiri', 'label-info'),
            ('Työpaja', 'label-warning'),
            ("Let's Play", 'label-danger'),
            ('Visa/leikki', 'label-primary'),
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                title=tag_name,
                defaults=dict(
                    style=tag_style,
                ),
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

            # Half hours
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(start_time, end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(
                    event=self.event,
                    start_time=hour_start_time.replace(minute=30)
                )

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
        from ...models import SignupExtra, SpecialDiet, EventDay
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
            contact_email='Yukiconin työvoimatiimi <yukicon@yukicon.fi>',
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

        for jc_data in [
            (
                'Conitea',
                'Tapahtuman järjestelytoimikunnan eli conitean jäsen',
                [conitea]
            ),
            (
                'Erikoistehtävä',
                'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, '
                'valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut '
                'on valittu.',
                [tyovoima]
            ),
            (
                'Info',
                'Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman '
                'aikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.',
                [tyovoima]
            ),
            (
                'Järjestyksenvalvoja',
                'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa '
                'JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole '
                'täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).',
                [tyovoima]
            ),
            (
                'Lipuntarkastaja',
                'Lipuntarkastajana hoidat e-lippujen vaihtoa rannekkeiksi ja tarkistat lippuja ovella. Tehtävä '
                'edellyttää asiakaspalveluasennetta.',
                [tyovoima]
            ),
            (
                'Logistiikka', 'Autokuskina toimimista ja tavaroiden/ihmisten hakua ja noutamista. B-luokan '
                'ajokortti vaaditaan. Työvuoroja myös perjantaille.',
                [tyovoima]
            ),
            (
                'Narikka',
                'Narikassa säilytetään tapahtuman aikana kävijöiden omaisuutta. Tehtävä ei vaadi erikoisosaamista.',
                [tyovoima]
            ),
            (
                'Pukuhuoneet',
                'Pukuhuonevänkärit vastaavat pukuhuoneiden siisteydestä ja viihtyvyydestä ja tarvittaessa auttavat '
                'cosplayaajia pukujensa kanssa.',
                [tyovoima]
            ),
            (
                'Salivänkäri',
                'Luennoitsijoiden ja muiden ohjelmanpitäjien avustamista ohjelmanumeroiden yhteydessä.',
                [tyovoima]
            ),
            (
                'Siivous',
                'Siivousvänkärit ovat vastuussa tapahtuman yleisestä siisteydestä. He kulkevat ympäriinsä '
                'tehtävänään roskakorien tyhjennys, vesipisteiden täyttö, vessoihin papereiden lisääminen '
                'ja monet muut pienet askareet. Työ tehdään pääsääntöisesti vänkäripareittain.',
                [tyovoima]
            ),
            (
                'Tekniikka',
                'Salitekniikan (AV) ja tietotekniikan (tulostimet, lähiverkot, WLAN) nopeaa MacGyver-henkistä '
                'ongelmanratkaisua.',
                [tyovoima]
            ),
            (
                'Valokuvaus',
                'Valokuvaus tapahtuu pääasiassa kuvaajien omilla järjestelmäkameroilla. Tehtäviä voivat olla '
                'studiokuvaus, salikuvaus sekä yleinen valokuvaus. Kerro Työkokemus-kentässä aiemmasta '
                'valokuvauskokemuksestasi (esim. linkkejä kuvagallerioihisi) sekä mitä/missä haluaisit '
                'tapahtumassa valokuvata.',
                [tyovoima]
            ),
            (
                'Yleisvänkäri',
                'Sekalaisia tehtäviä laidasta laitaan, jotka eivät vaadi erikoisosaamista. Voit halutessasi '
                'kirjata lisätietoihin, mitä osaat ja haluaisit tehdä.',
                [tyovoima]
            ),

            # ('Kasaus ja purku', 'Kalusteiden siirtelyä & opasteiden kiinnittämistä. Ei vaadi erikoisosaamista. Työvuoroja myös jo pe sekä su conin sulkeuduttua, kerro lisätiedoissa jos voit osallistua näihin.', [tyovoima]),
            # ('Majoitusvalvoja', 'Huolehtivat lattiamajoituspaikkojen pyörittämisestä yöaikaan. Työvuoroja myös molempina öinä.', [tyovoima]),
            # ('Green room', 'Työvoiman ruokahuolto green roomissa. Edellyttää hygieniapassia.', [tyovoima]),
            # ('Taltiointi', 'Taltioinnin keskeisiin tehtäviin kuuluvat mm. saleissa esitettävien ohjelmanumeroiden videointi tapahtumassa ja editointi tapahtuman jälkeen. Lisäksi videoidaan dokumentaarisella otteella myös yleisesti tapahtumaa. Kerro Työkokemus-kentässä aiemmasta videokuvauskokemuksestasi (esim. linkkejä videogallerioihisi) sekä mitä haluaisit taltioinnissa tehdä.', [tyovoima]),
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

        for name in ['Conitea']:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ('Järjestyksenvalvoja', 'JV-kortti'),
            ('Logistiikka', 'Henkilöauton ajokortti (B)'),
            # ('Green room', 'Hygieniapassi'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)
            if not jc.required_qualifications.exists():
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

        for event_day in [
            'Pyrycon – Perjantai 17.2.2017',
            'Yukicon 4.0 – Lauantai 18.2.2017',
            'Yukicon 4.0 – Sunnuntai 19.2.2017',
        ]:
            EventDay.objects.get_or_create(name=event_day)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug='conitea',
            defaults=dict(
                title='Conitean ilmoittautumislomake',
                signup_form_class_path='events.yukicon2017.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.yukicon2017.forms:OrganizerSignupExtraForm',
                active_from=datetime(2016, 6, 30, 0, 0, 0, tzinfo=self.tz),
                active_until=self.event.start_time,
            ),
        )

        for wiki_space, link_title, link_group in [
            # ('YUKIWORK', 'Työvoimawiki', 'accepted'),
            # ('YUKINFO', 'Infowiki', 'info'),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url='https://confluence.tracon.fi/display/{wiki_space}'.format(wiki_space=wiki_space),
                    group=labour_event_meta.get_group(link_group),
                )
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


class Command(BaseCommand):
    args = ''
    help = 'Setup yukicon2017 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
