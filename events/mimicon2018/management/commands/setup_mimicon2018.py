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
        from core.models import Venue, Event, Organization

        self.venue, unused = Venue.objects.get_or_create(name='Kongressitalo Mikaeli', defaults=dict(
            name_inessive='Kongressitalo Mikaelissa',
        ))
        self.organization, unused = Organization.objects.get_or_create(
            slug='mamy-mikkelin-anime-ja-manga-yhdistys-ry',
            defaults=dict(
                name='MAMY Mikkelin Anime ja Manga Yhdistys ry',
                homepage_url='http://mamy.animeunioni.org/',
            )
        )
        self.event, unused = Event.objects.get_or_create(slug='mimicon2018', defaults=dict(
            name='Mimicon (2018)',
            name_genitive='Mimiconiin',
            name_illative='Mimiconia',
            name_inessive='Mimiconissa',
            homepage_url='https://mimicon.moe',
            organization=self.organization,
            start_time=datetime(2018, 9, 15, 10, 0, tzinfo=self.tz),
            end_time=datetime(2018, 9, 16, 18, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, = TicketsEventMeta.get_or_create_groups(self.event, ['admins'])

        defaults = dict(
            admin_group=tickets_admin_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2018{:05d}",
            contact_email='Mimicon <lipunmyynti@mimicon.moe>',
            ticket_free_text="Tämä on sähköinen lippusi Mimicon 2018 -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa Mimiconiin!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Mimicon 2018 -tapahtumaan!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://www.mimicon.moe'>Mimiconin kotisivuilta</a>.</p>",
            # print_logo_path = mkpath('static', 'images', 'mimicon2018_logo.png'),
            print_logo_width_mm = 30,
            print_logo_height_mm = 30,
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

        def ordering():
            ordering.counter += 10
            return ordering.counter
        ordering.counter = 0

        for product_info in [
            dict(
                name='Mimicon 2018 -pääsylippu',
                description='Viikonloppulippu Mimicon 2018-tapahtumaan (la-su(. Sähköinen lippu vaihdetaan rannekkeeseen tapahtumapaikalla.',
                limit_groups=[
                    limit_group('Pääsyliput', 500),
                ],
                price_cents=1800,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=ordering(),
            ),
            # dict(
            #     name='Lattiamajoituspaikka',
            #     description='Lattiamajoituspaikka lauantain ja sunnuntain väliseksi yöksi. Tarvitset oman makuupussin ja -alustan. Lattiamajoituksesta ei lähetetä erillistä lippua, vaan lattiamajoitus toimii nimi listaan -periaatteella.',
            #     limit_groups=[
            #         limit_group('Lattiamajoitus', 80),
            #     ],
            #     price_cents=500,
            #     requires_shipping=False,
            #     electronic_ticket=False,
            #     available=True,
            #     ordering=ordering(),
            # ),
            # dict(
            #     name='Lounaslippu',
            #     description='Tällä lipukkeella saat herkullisen lounaan ravintola Napostellasta kumpana tahansa tapahtumapäivänä. Lounasliput toimitetaan samalla PDF-lipulla pääsylippujesi kanssa.',
            #     limit_groups=[
            #         limit_group('Lounas', 100),
            #     ],
            #     price_cents=780,
            #     requires_shipping=False,
            #     electronic_ticket=True,
            #     available=False,
            #     ordering=ordering(),
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
            work_begins=self.event.start_time - timedelta(days=1),
            work_ends=self.event.end_time + timedelta(hours=4),
            admin_group=labour_admin_group,
            contact_email='Mimiconin työvoimavastaava <tyovoima@mimicon.moe>',
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

        if not JobCategory.objects.filter(event=self.event).exists():
            for jc_data in [
                ("Conitea", "Tapahtuman conitean eli järjestelytoimikunnan jäsen.", [conitea]),
                ("Erikoistehtävä", "Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.", [tyovoima]),
                ("Järjestyksenvalvoja", "Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi > Pätevyydet).", [tyovoima]),
                ("Ensiapu", "Tapahtuman ensiapupisteellä avustaminen. Edellyttää voimassa olevaa EA1-korttia. EA2-kortti luonnollisesti plussaa. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi EA1-korttisi numeroa (oikealta ylhäältä oma nimesi > Pätevyydet)", [tyovoima]),
                ("Info", "Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman aikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä. Mimiconissa infon tehtäviin kuuluu hiljaisina hetkinä myös kevyttä yleisvänkäröintiä, joihin saat tapahtumapaikalla lisäohjeita.", [tyovoima]),
                ("Lipunmyynti", "Lipuntarkastajana hoidat e-lippujen vaihtoa rannekkeiksi, sekä mahdollisesti lippujen myyntiä ovelta. Tehtävä edellyttää asiakaspalveluasennetta ja rahankäsittelytaitoja.", [tyovoima]),
                ("Narikka", "Narikassa säilytetään tapahtuman aikana kävijöiden omaisuutta. Tehtävä ei vaadi erikoisosaamista.", [tyovoima]),
                ("Ohjelma-avustaja", "Luennoitsijoiden ja muiden ohjelmanpitäjien avustamista ohjelmanumeroiden yhteydessä. He pitävät huolen, että ohjelmat alkavat ja loppuvat ajallaan ja että ohjelmanjärjestäjillä on kaikki mitä he tarvitsevat salissa.", [tyovoima]),
                ("Siivous", "Siivousvänkärit ovat vastuussa tapahtuman yleisestä siisteydestä. He kulkevat ympäriinsä tehtävänään roskakorien tyhjennys, vesipisteiden täyttö, vessoihin papereiden lisääminen ja monet muut pienet askareet.", [tyovoima]),
                ("Majoitusvalvoja", "Majoitusvalvojat vahtivat väsyneiden kävijöiden ja vänkäreiden unta majoituskoululla. Tehtävässä työskennellään yöllä, joten se edellyttää 18-vuoden ikää.", [tyovoima]),
                ("Kirpputori", "Kirpputorilla vastaanotat kävijöiden myyntiin tuomia tuotteita, ja myyt ne eteenpäin uusille omistajille. Kaikista myynneistä pidetään kirjanpitoa. Tehtävä edellyttää asiakaspalveluasennetta, tarkkuutta ja rahankäsittelytaitoja.", [tyovoima]),
                ("Pelihuone", "Pelihuoneella avustat ja valvot kävijöitä. Tehtävä ei vaadi erikoisosaamista.", [tyovoima]),
                ("Green room", "Green roomissa valmistetaan nälkäisille vänkäreille sekä kevyttä välipalaa että ruokaa. Green roomissa työskentelevät huolehtivat myös tilan siisteydestä. Tehtävä edellyttää hygieniapassia.", [tyovoima]),
                ("Kasaus ja purku", "Mimiconia kasataan tapahtumaa edeltävänä perjantaina, ja puretaan sunnuntaina ovien sulkeuduttua. Jos siis olet paikalla, tervetuloa mukaan! Tehtävä ei vaadi erikoisosaamista.", [tyovoima]),
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
                    job_category.personnel_classes.set(pcs)


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
            # ('Järjestyksenvalvoja', 'JV-kortti'),
            # ('Ensiapu', 'Ensiapukoulutus EA1'),
            # ('Logistiikka', u'Henkilöauton ajokortti (B)'),
            # ('Green room', 'Hygieniapassi'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)
            if not jc.required_qualifications.exists():
                jc.required_qualifications.set([qual])


        for diet_name in [
            'Gluteeniton',
            'Laktoositon',
            'Maidoton',
            'Vegaaninen',
            'Lakto-ovo-vegetaristinen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        for night_name in [
            'Perjantain ja lauantain välinen yö',
            'Lauantain ja sunnuntain välinen yö',
        ]:
            Night.objects.get_or_create(name=night_name)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug='conitea',
            defaults=dict(
                title='Conitean ilmoittautumislomake',
                signup_form_class_path='events.mimicon2018.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.mimicon2018.forms:OrganizerSignupExtraForm',
                active_from=datetime(2018, 4, 2, 12, 0, 0, tzinfo=self.tz),
                active_until=self.event.start_time,
            ),
        )

        for wiki_space, link_title, link_group in [
            # ('MIMIWORK', 'Työvoimawiki', 'accepted'),
            # ('MIMINFO', 'Infowiki', 'info'),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url='https://confluence.tracon.fi/display/{wiki_space}'.format(wiki_space=wiki_space),
                    group=labour_event_meta.get_group(link_group),
                )
            )

    def setup_programme(self):
        from labour.models import PersonnelClass
        from programme.models import (
            AlternativeProgrammeForm,
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

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ['admins', 'hosts'])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            public=False,
            admin_group=programme_admin_group,
            contact_email='Mimiconin ohjelmavastaava <ohjelma@mimicon.moe>',
            schedule_layout='reasonable',
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

        have_categories = Category.objects.filter(event=self.event).exists()
        if not have_categories:
            for title, style in [
                ('Luento', 'color1'),
                ('Paneeli', 'color2'),
                ('Esitys', 'color3'),
                ('Työpaja', 'color4'),
                ('Muu ohjelma', 'color5'),
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
                self.event.start_time,
                self.event.start_time.replace(hour=18, tzinfo=self.tz),
            ),
            (
                self.event.end_time.replace(hour=9, tzinfo=self.tz),
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
            start_time=self.event.start_time.replace(hour=10, minute=30, tzinfo=self.tz),
        )

        for tag_title, tag_class in [
            # ('Suositeltu', 'hilight'),
            # ('Musiikki', 'label-info'),
            # ('In English', 'label-success'),
            # ('K-18', 'label-danger'),
            # ('Paikkaliput', 'label-warning'),
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                title=tag_title,
                defaults=dict(
                    style=tag_class,
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
                real_name_must_be_visible=True,
            )
        )


class Command(BaseCommand):
    args = ''
    help = 'Setup mimicon2018 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
