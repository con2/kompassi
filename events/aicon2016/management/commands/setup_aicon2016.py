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
        self.setup_tickets()
        self.setup_access()
        self.setup_payments()
        self.setup_programme()

    def setup_core(self):
        from core.models import Venue, Event, Organization

        self.organization = Organization.objects.get(slug='aicon-ry')
        self.venue, unused = Venue.objects.get_or_create(
            name='Verkatehdas',
            name_inessive='Verkatehtaalla',
        )
        self.event, unused = Event.objects.get_or_create(slug='aicon2016', defaults=dict(
            name='Aicon',
            name_genitive='Aiconin',
            name_illative='Aiconiin',
            name_inessive='Aiconissa',
            homepage_url='http://2016.aicon.fi',
            organization=self.organization,
            start_time=datetime(2016, 10, 8, 10, 0, tzinfo=self.tz),
            end_time=datetime(2016, 10, 9, 18, 0, tzinfo=self.tz),
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
        from ...models import SignupExtra, SpecialDiet
        from django.contrib.auth.models import Group
        from django.contrib.contenttypes.models import ContentType

        labour_admin_group, created = Group.objects.get_or_create(name='aicon-staff')

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2016, 10, 7, 8, 0, tzinfo=self.tz),
            work_ends=datetime(2016, 10, 9, 22, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Aicon-työvoimatiimi <tyovoima@aicon.fi>',
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )
        else:
            # TODO once we know when the registration opens
            # labour_event_meta_defaults.update(
            #     registration_opens=datetime(2014, 3, 1, 0, 0, tzinfo=self.tz),
            #     registration_closes=datetime(2014, 8, 1, 0, 0, tzinfo=self.tz),
            # )
            pass

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            ('Vastaava', 'vastaava', 'labour'),
            ('Vuorovastaava', 'vuorovastaava', 'labour'),
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
        vuorovastaava = PersonnelClass.objects.get(event=self.event, slug='vuorovastaava')
        # ohjelma = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        # XXX
        if JobCategory.objects.filter(event=self.event).exists():
            return

        for jc_data in [
            ('Vastaava', 'Tapahtuman järjestäjä', [vastaava]),

            ('Erikoistehtävä', 'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.', [tyovoima, vuorovastaava]),
            ('Järjestyksenvalvoja', 'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).', [tyovoima, vuorovastaava]),
            ('Ensiapu', 'Toimit osana tapahtuman omaa ensiapuryhmää. Vuoroja päivisin ja öisin tapahtuman aukioloaikoina. Vaaditaan vähintään voimassa oleva EA1 -kortti ja osalta myös voimassa oleva EA2 -kortti. Kerro Työkokemus -kohdassa osaamisestasi, esim. oletko toiminut EA-tehtävissä tapahtumissa tai oletko sairaanhoitaja/lähihoitaja koulutuksestaltasi.', [tyovoima, vuorovastaava]),
            ('Kasaus ja purku', 'Kalusteiden siirtelyä & opasteiden kiinnittämistä. Ei vaadi erikoisosaamista. Työvuoroja myös jo pe sekä su conin sulkeuduttua, kerro lisätiedoissa jos voit osallistua näihin.', [tyovoima, vuorovastaava]),
            ('Logistiikka', 'Autokuskina toimimista ja tavaroiden/ihmisten hakua ja noutamista. B-luokan ajokortti vaaditaan. Työvuoroja myös perjantaille.', [tyovoima, vuorovastaava]),
            ('Majoitusvalvoja', 'Huolehtivat lattiamajoituspaikkojen pyörittämisestä yöaikaan. Työvuoroja myös molempina öinä.', [tyovoima, vuorovastaava]),
            ('myynti', 'Lipunmyynti ja narikka', 'Pääsylippujen ja oheistuotteiden myyntiä sekä lippujen tarkastamista. Myyjiltä edellytetään täysi-ikäisyyttä, asiakaspalveluhenkeä ja huolellisuutta rahankäsittelyssä. Vuoroja myös perjantaina.', [tyovoima, vuorovastaava]),
            ('info', 'Info-, ohjelma- ja yleisvänkäri', 'Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman paikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.', [tyovoima, vuorovastaava]),

            # ('Ohjelmanpitäjä', 'Luennon tai muun vaativan ohjelmanumeron pitäjä', [ohjelma]),
        ]:
            if len(jc_data) == 3:
                name, description, pcs = jc_data
                slug = slugify(name)
            elif len(jc_data) == 4:
                slug, name, description, pcs = jc_data

            job_category, created = JobCategory.objects.get_or_create(
                event=self.event,
                slug=slug,
                defaults=dict(
                    name=name,
                    description=description,
                )
            )

            if created:
                job_category.personnel_classes = pcs
                job_category.save()

        labour_event_meta.create_groups()

        for name in ['Vastaava']:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ('Järjestyksenvalvoja', 'JV-kortti'),
            ('Logistiikka', 'Henkilöauton ajokortti (B)'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

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
            slug='vastaava',
            defaults=dict(
                title='Vastaavien ilmoittautumislomake',
                signup_form_class_path='events.aicon2016.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.aicon2016.forms:OrganizerSignupExtraForm',
                active_from=datetime(2015, 10, 27, 12, 0, 0, tzinfo=self.tz),
                active_until=datetime(2016, 10, 9, 23, 59, 59, tzinfo=self.tz),
            ),
        )

        for wiki_space, link_title, link_group in [
            # ('AICONWORK', 'Työvoimawiki', 'accepted'),
            # ('AICONINFO', 'Infowiki', 'info'),
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
            reference_number_template="2016{:05d}",
            contact_email='Aicon-lipunmyynti <lipunmyynti@aicon.fi>',
            plain_contact_email='lipunmyynti@aicon.fi',
            ticket_free_text="Tämä on sähköinen lippusi Aiconiin. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva Kissakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa Aiconiin!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Aiconiin!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta <a href='http://aicon.fi'>Aiconin kotisivuilta</a>.</p>"
                "<p>Huom! Tämä verkkokauppa palvelee ainoastaan asiakkaita, joilla on osoite Suomessa. Mikäli tarvitset "
                "toimituksen ulkomaille, ole hyvä ja ota sähköpostitse yhteyttä: <em>lipunmyynti@aicon.fi</em>"
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
            dict(
                name='Joukkorahoitus – Viikonloppulippu',
                description='Tällä lipulla sisäänpääsy Aiconiin koko tapahtuman ajan! Lisäksi saat nimesi nettisivuillemme tulevaan kiitoslistaan, sekä kiitoskortin ja kangasmerkin! Myymme tavallisia viikonloppulippuja vielä myöhemminkin, mutta varmista omasi jo nyt!',
                limit_groups=[
                    limit_group('Pääsyliput', 11),
                ],
                price_cents=3000,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Joukkorahoitus – VIP-lippu',
                description="""Aiconin kaikki VIP-liput ovat myynnissä joukkorahoituksessa! Tartu tilaisuuteen nyt, sillä toista ei välttämättä tule!
Aiconin VIP-lippu sisältää tietenkin koko viikonlopun sisäänpääsyn tapahtumaan, mutta myös muuta! VIP-lippuihin saatetaan julkistaa vielä lisää sisältöä lähempänä conia, mutta nämä edut ovat varmoja:
- VIP-lippulla pääset conin alkaessa vaihtamaan lippusi erillisestä VIP-jonosta
- Conin aikana käytössäsi on VIP-tila, jota ylläpitää läpi tapahtuman VIP-asiakkaiden viihtyvyydestä vastaava host tai hostess.
- VIP-tilasta on pääsy pääsaliin VIP-parvelle, joten et välttämättä tarvitse paikkalippua pääsalin ohjelmiin, toisin kuin muut conikävijät.
- Saat conista mukaasi VIP-tuotepussin.
Lisäksi saat nimesi nettisivuillamme julkaistavaan kiitoslistaan, sekä kiitoskortin ja kangasmerkin toimitettuna sinulle jo kevään aikana.""",
                limit_groups=[
                    limit_group('VIP-liput', 56),
                ],
                price_cents=5500,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Viikonloppulippu',
                description='Tällä lipulla sisäänpääsy Aiconiin koko tapahtuman ajan! Lippu toimitetaan sähköpostiisi PDF-muotoisena E-lippuna, jonka vaihdat rannekkeeseen tapahtumaan saapuessasi.',
                limit_groups=[
                    limit_group('Pääsyliput', 11),
                ],
                price_cents=2500,
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

    def setup_access(self):
        from access.models import Privilege, GroupPrivilege, EmailAliasDomain, EmailAliasType, GroupEmailAliasGrant

        cc_group = self.event.labour_event_meta.get_group('vastaava')
        domain = EmailAliasDomain.objects.get(domain_name='aicon.fi')

        for type_code, type_metavar in [
            ('events.aicon2016.email_aliases:requested_alias', 'aicon11tehtävä'),
        ]:
            alias_type, created = EmailAliasType.objects.get_or_create(
                domain=domain,
                account_name_code=type_code,
                defaults=dict(
                    metavar=type_metavar,
                )
            )

        for metavar in [
            'etunimi.sukunimi',
            'nick',
            'aicon11tehtävä',
        ]:
            alias_type = EmailAliasType.objects.get(domain__domain_name='aicon.fi', metavar=metavar)
            GroupEmailAliasGrant.objects.get_or_create(
                group=cc_group,
                type=alias_type,
                defaults=dict(
                    active_until=self.event.end_time,
                )
            )

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
            Tag,
            TimeBlock,
            View,
        )

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ['admins', 'hosts'])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            public=False,
            admin_group=programme_admin_group,
            contact_email='Aiconin ohjelmatiimi <ohjelma@aicon.fi>',
        ))

        for room_name in [
            'Vanaja-sali',
            'Luentosali',
            'Kokoushuone',
            'Studio',
        ]:
            Room.objects.get_or_create(
                venue=self.venue,
                name=room_name,
                defaults=dict(
                    order=self.get_ordering_number()
                )
            )

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
                ('Luento', 'color1'),
                ('Esittävä ohjelma', 'color2'),
                ('Miitti', 'color3'),
                ('Työpaja', 'color4'),
                ('Karaoke', 'color5'),
            ]:
                Category.objects.get_or_create(
                    event=self.event,
                    style=style,
                    defaults=dict(
                        title=title,
                    )
                )

        for tag_name, tag_style in [
            ('Suositeltu', 'hilight'),
            ('Paikkaliput', 'label-danger'),
            ('International', 'label-primary'),
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                title=tag_name,
                defaults=dict(
                    style=tag_style,
                ),
            )

        if self.test:
            # create some test programme
            Programme.objects.get_or_create(
                category=Category.objects.get(title='Luento', event=self.event),
                title='Yaoi-paneeli',
                defaults=dict(
                    description='Kika-kika tirsk',
                )
            )

        if not TimeBlock.objects.filter(event=self.event).exists():
            for start_time, end_time in [
                (
                    self.event.start_time.replace(hour=10, minute=0, tzinfo=self.tz),
                    self.event.start_time.replace(hour=20, minute=0, tzinfo=self.tz),
                ),
                (
                    self.event.end_time.replace(hour=10, minute=0, tzinfo=self.tz),
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

                for hour_start_time in full_hours_between(start_time, end_time)[:-1]:
                    SpecialStartTime.objects.get_or_create(
                        event=self.event,
                        start_time=hour_start_time.replace(minute=30)
                    )

        for view_name, room_names in [
            ('Pääohjelmatilat', [
                'Vanaja-sali',
                'Luentosali',
                'Kokoushuone',
                'Studio',
            ]),
        ]:
            rooms = [Room.objects.get(name__iexact=room_name, venue=self.venue)
                for room_name in room_names]

            view, created = View.objects.get_or_create(event=self.event, name=view_name)

            if created:
                view.rooms = rooms
                view.save()


class Command(BaseCommand):
    args = ''
    help = 'Setup aicon2016 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
