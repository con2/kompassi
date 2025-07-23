from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from kompassi.core.utils import full_hours_between, slugify


class Setup:
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
        self.setup_intra()
        # self.setup_tickets()
        # self.setup_programme()
        # self.setup_access()
        self.setup_badges()

    def setup_core(self):
        from kompassi.core.models import Event, Organization, Venue

        self.venue, unused = Venue.objects.get_or_create(
            name="Tredun Sammonkadun toimipiste",
            defaults=dict(
                name_inessive="Tredun Sammonkadun toimipisteessä",
            ),
        )
        self.organization = Organization.objects.get(slug="tracon-ry")
        self.event, unused = Event.objects.get_or_create(
            slug="hitpoint2019",
            defaults=dict(
                name="Tracon Hitpoint 2019",
                name_genitive="Tracon Hitpoint 2019 -tapahtuman",
                name_illative="Tracon Hitpoint 2019 -tapahtumaan",
                name_inessive="Tracon Hitpoint 2019 -tapahtumassa",
                homepage_url="http://2019.hitpoint.tracon.fi",
                organization=self.organization,
                start_time=datetime(2019, 11, 23, 10, 0, tzinfo=self.tz),
                end_time=datetime(2019, 11, 24, 18, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from kompassi.core.models import Person
        from kompassi.labour.models import (
            AlternativeSignupForm,
            InfoLink,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Qualification,
            Survey,
        )

        from ...models import SignupExtra, SpecialDiet

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2019, 11, 23, 8, 0, 0, tzinfo=self.tz),
            work_ends=datetime(2019, 11, 24, 23, 59, 59, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email="Tracon Hitpoint 2019 -työvoimatiimi <hitpoint@tracon.fi>",
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
            ("Conitea", "conitea", "labour"),
            ("Vuorovastaava", "ylivankari", "labour"),
            ("Työvoima", "tyovoima", "labour"),
            ("Ohjelmanjärjestäjä", "ohjelma", "programme"),
            ("Guest of Honour", "goh", "programme"),
            ("Media", "media", "badges"),
            ("Myyjä", "myyja", "badges"),
            ("Vieras", "vieras", "badges"),
            ("Vapaalippu", "vapaalippu", "badges"),
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

        tyovoima = PersonnelClass.objects.get(event=self.event, slug="tyovoima")
        conitea = PersonnelClass.objects.get(event=self.event, slug="conitea")
        ylivankari = PersonnelClass.objects.get(event=self.event, slug="ylivankari")
        ohjelma = PersonnelClass.objects.get(event=self.event, slug="ohjelma")

        if not JobCategory.objects.filter(event=self.event).exists():
            for jc_data in [
                ("Conitea", "Tapahtuman järjestelytoimikunnan eli conitean jäsen", [conitea]),
                (
                    "Erikoistehtävä",
                    "Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.",
                    [tyovoima, ylivankari],
                ),
                (
                    "Järjestyksenvalvoja",
                    "Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).",
                    [tyovoima, ylivankari],
                ),
                (
                    "Ensiapu",
                    "Toimit osana tapahtuman omaa ensiapuryhmää. Vuoroja päivisin ja öisin tapahtuman aukioloaikoina. Vaaditaan vähintään voimassa oleva EA1 -kortti ja osalta myös voimassa oleva EA2 -kortti. Kerro Työkokemus -kohdassa osaamisestasi, esim. oletko toiminut EA-tehtävissä tapahtumissa tai oletko sairaanhoitaja/lähihoitaja koulutuksestaltasi.",
                    [tyovoima, ylivankari],
                ),
                (
                    "Kasaus ja purku",
                    "Kalusteiden siirtelyä & opasteiden kiinnittämistä. Ei vaadi erikoisosaamista. Työvuoroja myös jo pe sekä su conin sulkeuduttua, kerro lisätiedoissa jos voit osallistua näihin.",
                    [tyovoima, ylivankari],
                ),
                (
                    "Logistiikka",
                    "Autokuskina toimimista ja tavaroiden/ihmisten hakua ja noutamista. B-luokan ajokortti vaaditaan. Työvuoroja myös perjantaille.",
                    [tyovoima, ylivankari],
                ),
                (
                    "Majoitusvalvoja",
                    "Huolehtivat lattiamajoituspaikkojen pyörittämisestä yöaikaan. Työvuoroja myös molempina öinä.",
                    [tyovoima, ylivankari],
                ),
                (
                    "myynti",
                    "Lipunmyynti ja narikka",
                    "Pääsylippujen ja Tracon-oheistuotteiden myyntiä sekä lippujen tarkastamista. Myyjiltä edellytetään täysi-ikäisyyttä, asiakaspalveluhenkeä ja huolellisuutta rahankäsittelyssä. Vuoroja myös perjantaina.",
                    [tyovoima, ylivankari],
                ),
                (
                    "info",
                    "Info-, ohjelma- ja yleisvänkäri",
                    "Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman paikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.",
                    [tyovoima, ylivankari],
                ),
                ("Ohjelmanpitäjä", "Luennon tai muun vaativan ohjelmanumeron pitäjä", [ohjelma]),
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
                    ),
                )

                if created:
                    job_category.personnel_classes.set(pcs)

        labour_event_meta.create_groups()

        for name in ["Conitea"]:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ("Järjestyksenvalvoja", "JV-kortti"),
            ("Logistiikka", "Henkilöauton ajokortti (B)"),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

        for diet_name in [
            "Gluteeniton",
            "Laktoositon",
            "Maidoton",
            "Vegaaninen",
            "Lakto-ovo-vegetaristinen",
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="conitea",
            defaults=dict(
                title="Conitean ilmoittautumislomake",
                signup_form_class_path="events.hitpoint2019.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.hitpoint2019.forms:OrganizerSignupExtraForm",
                active_from=datetime(2018, 12, 28, 12, 0, 0, tzinfo=self.tz),
                active_until=datetime(2019, 11, 24, 23, 59, 59, tzinfo=self.tz),
            ),
        )

        Survey.objects.get_or_create(
            event=self.event,
            slug="swag",
            defaults=dict(
                title="Swag",
                description=("Syötä tässä paitakokosi, jos haluat työvoimapaidan."),
                form_class_path="events.hitpoint2019.forms:SwagSurvey",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

        for wiki_space, link_title, link_group in [
            ("HITPOINT2019", "Coniteawiki", "conitea"),
            ("HTPTWORK", "Työvoimawiki", "accepted"),
            ("HTPTINFO", "Infowiki", "info"),
        ]:
            InfoLink.objects.get_or_create(
                event=self.event,
                title=link_title,
                defaults=dict(
                    url=f"https://confluence.tracon.fi/display/{wiki_space}",
                    group=labour_event_meta.get_group(link_group),
                ),
            )

    def setup_programme(self):
        from kompassi.labour.models import PersonnelClass
        from kompassi.zombies.programme.models import (
            AlternativeProgrammeForm,
            Category,
            ProgrammeEventMeta,
            Role,
            SpecialStartTime,
            TimeBlock,
        )

        from ...models import TimeSlot

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins", "hosts"])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                public=False,
                admin_group=programme_admin_group,
                contact_email="Tracon Hitpoint -ohjelmatiimi <hitpoint.ohjelma@tracon.fi>",
                schedule_layout="reasonable",
            ),
        )

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        for pc_slug, role_title, role_is_default in [
            ("ohjelma", "Ohjelmanjärjestäjä", True),
            # ('ohjelma-2lk', 'Ohjelmanjärjestäjä (2. luokka)', False),
            # ('ohjelma-3lk', 'Ohjelmanjärjestäjä (3. luokka)', False),
        ]:
            personnel_class = PersonnelClass.objects.get(event=self.event, slug=pc_slug)
            role, unused = Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_is_default,
                ),
            )

        have_categories = Category.objects.filter(event=self.event).exists()
        if not have_categories:
            for title, slug, style in [
                ("Larp", "larp", "color1"),
                ("Lautapelit", "lautapelit", "color2"),
                ("Puheohjelma", "puheohjelma", "color3"),
                ("Roolipeli", "roolipeli", "color4"),
                ("Freeform", "freeform", "color1"),
                ("Korttipelit", "korttipelit", "color5"),
                ("Figupelit", "figupelit", "color6"),
                ("Muu ohjelma", "muu-ohjelma", "color7"),
                ("Sisäinen ohjelma", "sisainen-ohjelma", "sisainen"),
            ]:
                Category.objects.get_or_create(
                    event=self.event,
                    slug=slug,
                    defaults=dict(
                        title=title,
                        style=style,
                        public=style != "sisainen",
                    ),
                )

        for start_time, end_time in [
            (
                datetime(2019, 11, 23, 10, 0, tzinfo=self.tz),
                datetime(2019, 11, 24, 1, 0, tzinfo=self.tz),
            ),
            (
                datetime(2019, 11, 24, 9, 0, tzinfo=self.tz),
                datetime(2019, 11, 24, 18, 0, tzinfo=self.tz),
            ),
        ]:
            TimeBlock.objects.get_or_create(event=self.event, start_time=start_time, defaults=dict(end_time=end_time))

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(event=self.event, start_time=hour_start_time.replace(minute=30))

        AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="rpg",
            defaults=dict(
                title="Tarjoa pöytäroolipeliä",
                description="",
                programme_form_code="events.hitpoint2019.forms:RpgForm",
                num_extra_invites=0,
                order=10,
            ),
        )

        AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="freeform",
            defaults=dict(
                title="Tarjoa freeform-skenaariota",
                short_description="",
                programme_form_code="events.hitpoint2019.forms:FreeformForm",
                num_extra_invites=0,
                order=20,
            ),
        )

        AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="default",
            defaults=dict(
                title="Tarjoa puhe- tai muuta ohjelmaa",
                short_description="Valitse tämä vaihtoehto, mikäli ohjelmanumerosi ei ole roolipeli tai freeform-skenaario.",
                programme_form_code="programme.forms:ProgrammeOfferForm",
                num_extra_invites=0,
                order=30,
            ),
        )

        for time_slot_name in [
            "Lauantaina päivällä",
            "Lauantaina iltapäivällä",
            "Lauantaina illalla",
            "Lauantain ja sunnuntain välisenä yönä",
            "Sunnuntaina aamupäivällä",
            "Sunnuntaina päivällä",
        ]:
            TimeSlot.objects.get_or_create(name=time_slot_name)

    def setup_tickets(self):
        from kompassi.zombies.tickets.models import LimitGroup, Product, TicketsEventMeta

        (tickets_admin_group,) = TicketsEventMeta.get_or_create_groups(self.event, ["admins"])

        defaults = dict(
            admin_group=tickets_admin_group,
            reference_number_template="2019{:06d}",
            contact_email="Tracon Hitpoint -lipunmyynti <hitpoint@tracon.fi>",
            ticket_free_text="Tämä on sähköinen lippusi Tracon Hitpoint -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
            "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
            "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
            "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva Kissakoodi ja ilmoita se\n"
            "lipunvaihtopisteessä.\n\n"
            "Tervetuloa Tracon Hitpointiin!",
            front_page_text="<h2>Tervetuloa ostamaan pääsylippuja Tracon Hitpoint -tapahtumaan!</h2>"
            "<p>Liput maksetaan suomalaisilla verkkopankkitunnuksilla heti tilauksen yhteydessä.</p>"
            "<p>Lue lisää tapahtumasta <a href='http://2019.hitpoint.tracon.fi'>Tracon Hitpoint -tapahtuman kotisivuilta</a>.</p>"
            "<p>Huom! Tämä verkkokauppa palvelee ainoastaan asiakkaita, joilla on osoite Suomessa. Mikäli tarvitset "
            "toimituksen ulkomaille, ole hyvä ja ota sähköpostitse yhteyttä: <em>hitpoint@tracon.fi</em>",
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            # TODO
            defaults.update(
                ticket_sales_starts=datetime(2019, 9, 14, 18, 0, tzinfo=self.tz),
                ticket_sales_ends=self.event.end_time,
            )
            pass

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
                name="Tracon Hitpoint -pääsylippu",
                description="Viikonloppulippu Tracon Hitpoint 2019-tapahtumaan. Voimassa koko viikonlopun ajan la klo 10–00 ja su klo 10–18. Toimitetaan sähköpostitse PDF-tiedostona, jossa olevaa viivakoodia vastaan saat rannekkeen tapahtumaan saapuessasi.",
                limit_groups=[
                    limit_group("Pääsyliput", 800),
                ],
                price_cents=1000,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
        ]:
            name = product_info.pop("name")
            limit_groups = product_info.pop("limit_groups")

            product, unused = Product.objects.get_or_create(event=self.event, name=name, defaults=product_info)

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)
                product.save()

    def setup_access(self):
        from kompassi.access.models import EmailAliasType, GroupEmailAliasGrant, GroupPrivilege, Privilege

        # Grant accepted workers access to Tracon Slack
        group = self.event.labour_event_meta.get_group("accepted")
        privilege = Privilege.objects.get(slug="tracon-slack")
        GroupPrivilege.objects.get_or_create(group=group, privilege=privilege, defaults=dict(event=self.event))

        cc_group = self.event.labour_event_meta.get_group("conitea")

        for metavar in [
            "etunimi.sukunimi",
            "nick",
        ]:
            alias_type = EmailAliasType.objects.get(domain__domain_name="tracon.fi", metavar=metavar)
            GroupEmailAliasGrant.objects.get_or_create(
                group=cc_group,
                type=alias_type,
                defaults=dict(
                    active_until=self.event.end_time,
                ),
            )

    def setup_badges(self):
        from kompassi.badges.models import BadgesEventMeta

        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
            ),
        )

    def setup_intra(self):
        from kompassi.intra.models import IntraEventMeta, Team

        (admin_group,) = IntraEventMeta.get_or_create_groups(self.event, ["admins"])
        organizer_group = self.event.labour_event_meta.get_group("conitea")
        meta, unused = IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            ),
        )

        for team_slug, team_name in [
            ("tuottajat", "Tuottajat"),
            ("infra", "Infra"),
            ("palvelut", "Palvelut"),
            ("ohjelma", "Ohjelma"),
        ]:
            (team_group,) = IntraEventMeta.get_or_create_groups(self.event, [team_slug])
            Team.objects.get_or_create(
                event=self.event,
                slug=team_slug,
                defaults=dict(
                    name=team_name,
                    order=self.get_ordering_number(),
                    group=team_group,
                ),
            )


class Command(BaseCommand):
    args = ""
    help = "Setup hitpoint2019 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
