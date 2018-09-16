from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.utils import full_hours_between, slugify


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
        self.setup_badges()
        self.setup_programme()
        self.setup_intra()

    def setup_core(self):
        from core.models import Venue, Event

        self.venue, unused = Venue.objects.get_or_create(name='Kulttuuritalo (Helsinki)', defaults=dict(
            name_inessive='Kulttuuritalossa Helsingissä',
        ))
        self.event, unused = Event.objects.get_or_create(slug='aicon2018', defaults=dict(
            name='Aicon (2018)',
            name_genitive='Aiconin',
            name_illative='Aiconiin',
            name_inessive='Aiconissa',
            homepage_url='http://2018.aicon.fi',
            organization_name='Aicon ry',
            organization_url='http://aicon.fi',
            start_time=datetime(2018, 7, 7, 10, 0, tzinfo=self.tz),
            end_time=datetime(2018, 7, 7, 18, 0, tzinfo=self.tz),
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
            contact_email='Aicon <liput@aicon.fi>',
            ticket_free_text=(
                "Tämä on sähköinen lippusi. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva sanakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa tapahtumaan!"
            ),
            front_page_text=(
                "<h2>Tervetuloa ostamaan pääsylippuja vuoden 2018 Aiconiin!</h2>"
                "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
                "<p>Lue lisää tapahtumasta "
                "<a href='http://2018.aicon.fi' target='_blank'>Aiconin kotisivuilta</a>.</p>"
            ),
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
                name='VIP-lippu',
                description='Koko viikonlopun lippu Aiconiin huikein VIP-eduin!',
                limit_groups=[
                    limit_group('VIP-liput', 50),
                ],
                price_cents=3000,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Pääsylippu',
                description='Koko viikonlopun lippu Aiconiin.',
                limit_groups=[
                    limit_group('Viikonloppuliput', 800),
                ],
                price_cents=1500,
                requires_shipping=False,
                electronic_ticket=True,
                available=False,
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
            work_begins=self.event.start_time.replace(hour=8, minute=0, tzinfo=self.tz),
            work_ends=self.event.end_time.replace(hour=22, minute=0, tzinfo=self.tz),
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
                signup_form_class_path='events.aicon2018.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.aicon2018.forms:OrganizerSignupExtraForm',
                active_from=datetime(2018, 4, 26, 12, 0, 0, tzinfo=self.tz),
                active_until=self.event.end_time,
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

    def setup_programme(self):
        from django.contrib.auth.models import Group
        from labour.models import PersonnelClass
        from programme.models import (
            Category,
            ProgrammeEventMeta,
            Role,
            SpecialStartTime,
            Tag,
            TimeBlock,
        )
        from core.utils import full_hours_between

        admin_group, hosts_group = Group.objects.get_or_create(name='aicon-staff')
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            admin_group=admin_group,
        ))

        if not programme_event_meta.contact_email:
            programme_event_meta.contact_email = 'Aiconin ohjelmavastaava <ohjelma@aicon.fi>'
            programme_event_meta.save()

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

        for category_name, category_style in [
            ('Esittävä ohjelma', 'color1'),
            ('Karaoke', 'color2'),
            ('Luento', 'color3'),
            ('Miitti', 'color4'),
            ('Työpaja', 'color5'),
        ]:
            Category.objects.get_or_create(
                event=self.event,
                title=category_name,
                defaults=dict(
                    style=category_style,
                )
            )

        for tag_name, tag_style in [
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

        if not TimeBlock.objects.filter(event=self.event).exists():
            for start_time, end_time in [
                (
                    self.event.start_time.replace(hour=11, tzinfo=self.tz),
                    self.event.start_time.replace(hour=17, tzinfo=self.tz),
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
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(
                    event=self.event,
                    start_time=hour_start_time.replace(minute=30)
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

    def setup_intra(self):
        from intra.models import IntraEventMeta, Team

        admin_group, = IntraEventMeta.get_or_create_groups(self.event, ['admins'])
        organizer_group = self.event.labour_event_meta.get_group('vastaava')
        meta, unused = IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            )
        )

        for team_slug, team_name in [
            ('vastaavat', 'Vastaavat'),
        ]:
            team_group, = IntraEventMeta.get_or_create_groups(self.event, [team_slug])

            team, created = Team.objects.get_or_create(
                event=self.event,
                slug=team_slug,
                defaults=dict(
                    name=team_name,
                    order=self.get_ordering_number(),
                    group=team_group,
                )
            )



class Command(BaseCommand):
    args = ''
    help = 'Setup aicon2018 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
