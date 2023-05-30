from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.conf import settings
from dateutil.tz import tzlocal
from django.utils.timezone import now

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
        self.setup_badges()
        # self.setup_tickets()
        self.setup_programme()
        self.setup_intra()
        # self.setup_access()
        self.setup_directory()
        # self.setup_kaatoilmo()
        # self.setup_sms()

    def setup_core(self):
        from core.models import Organization, Venue, Event

        self.organization, unused = Organization.objects.get_or_create(
            slug="paakaupunkiseudus-cosplay-ry",
            defaults=dict(
                name="Pääkaupunkiseudun Cosplay ry",
                homepage_url="https://pkscosplay.wordpress.com/",
            ),
        )
        self.venue, unused = Venue.objects.get_or_create(
            name="Kulttuurikeskus Stoa",
            defaults=dict(
                name_inessive="Kulttuurikeskus Stoassa",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="shumicon2023",
            defaults=dict(
                public=True,
                name="Shumicon 2023",
                name_genitive="Shumiconissa",
                name_illative="Shumiconiin",
                name_inessive="Shumiconissa",
                homepage_url="https://shumicon.fi",
                organization=self.organization,
                start_time=datetime(2023, 10, 21, 10, 0, tzinfo=self.tz),
                end_time=datetime(2023, 10, 22, 19, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from core.models import Event, Person
        from core.utils import slugify
        from labour.models import (
            AlternativeSignupForm,
            InfoLink,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Qualification,
            Survey,
        )
        from ...models import SignupExtra, SpecialDiet, KnownLanguage, NativeLanguage
        from django.contrib.contenttypes.models import ContentType

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time.replace(hour=8, minute=0, tzinfo=self.tz),
            work_ends=self.event.end_time.replace(hour=22, minute=0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email="Shumicon <tyovoima@shumicon.fi>",
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

        for pc_prio, pc_name, pc_slug, pc_app_label in [
            (10, "Vastaavat", "vastaava", "labour"),
            (20, "Työvoima", "tyovoima", "labour"),
            (30, "Ohjelmanjärjestäjä", "ohjelma", "programme"),
        ]:
            personnel_class, created = PersonnelClass.objects.get_or_create(
                event=self.event,
                slug=pc_slug,
                defaults=dict(
                    name=pc_name,
                    app_label=pc_app_label,
                    priority=pc_prio,
                ),
            )

        tyovoima = PersonnelClass.objects.get(event=self.event, slug="tyovoima")
        vastaava = PersonnelClass.objects.get(event=self.event, slug="vastaava")

        if not JobCategory.objects.filter(event=self.event).exists():
            for jc_data in [
                ("vastaava", "Vastaava", "Tapahtuman järjestelytoimikunnan jäsen", [vastaava]),
                #(
                #    "jv",
                #    "Järjestyksenvalvoja",
                #    "Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).",
                #    [tyovoima],
                #),
                (
                    "greenroom",
                    "Greenroom",
                    "Pidät huolta että meidän vapaaehtoisille riittää kahvia ja muuta naposteltavaa takahuoneessa. HUOM! Vaatii hygieniapassin",
                    [tyovoima],
                ),
                (
                    "info",
                    "Info",
                    "Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman paikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.",
                    [tyovoima],
                ),
                (
                    "karaoke",
                    "Karaoke",
                    "Kun mieli tahtoo laulaa, on mentävä karaokeen. Tässä tehtävässä et niinkään pääse itse laulamaan vaan hoidat karaokepistettä muiden iloksi",
                    [tyovoima],
                ),
                (
                    "rannekkeenvaihto",
                    "Rannekkeenvaihto",
                    "Etukäteen ostettujen lippujen tarkistaminen ja vaihtaminen rannekkeisiin",
                    [tyovoima],
                ),
                (
                    "ohjelmajuoksija",
                    "Ohjelmajuoksija",
                    "Avustaa ohjelmanjärjestäjiä salitekniikan ja ohjelmanumeron käynnistämisessä.",
                    [tyovoima],
                ),
                (
                    "narikka",
                    "Narikka",
                    "Syksyllä on jo pimeää ja kylmää, joten ihmisillä on takit päällä. Tapahtuman ajaksi ne kannattaa jättää narikkaan säilöön.",
                    [tyovoima],
                ),
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

        for slug in ["vastaava"]:
            JobCategory.objects.filter(event=self.event, slug=slug).update(public=False)

        for jc_name, qualification_name in [
            ("Järjestyksenvalvoja", "JV-kortti"),
            ("Greenroom", "Hygieniapassi"),
        ]:
            try:
                jc = JobCategory.objects.get(event=self.event, name=jc_name)
                qual = Qualification.objects.get(name=qualification_name)
                jc.required_qualifications.set([qual])
            except JobCategory.DoesNotExist:
                pass

        for language in [
            "Suomi",
            "Ruotsi",
            "Englanti",
            "Venäjä",
            "Somali",
            "Muu, mikä?"
        ]:
            NativeLanguage.objects.get_or_create(name=language)

        for language in [
            "Suomi",
            "Ruotsi",
            "Englanti",
            "Venäjä",
            "Somali",
            "Viittomakieli",
        ]:
            KnownLanguage.objects.get_or_create(name=language)

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
            slug="vastaava",
            defaults=dict(
                title="Vastaavien ilmoittautumislomake",
                signup_form_class_path="events.shumicon2023.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.shumicon2023.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

    def setup_badges(self):
        from badges.models import BadgesEventMeta

        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                badge_layout="nick",
                real_name_must_be_visible=True,
            ),
        )

    def setup_programme(self):
        from core.utils import full_hours_between
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

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins", "hosts"])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                public=False,
                admin_group=programme_admin_group,
                contact_email="Shumicon ohjelmatiimi <ohjelma@shumicon.fi>",
                schedule_layout="full_width",
            ),
        )

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        for pc_slug, role_title, role_is_default in [
            ("ohjelma", "Ohjelmanjärjestäjä", True),
        ]:
            personnel_class = PersonnelClass.objects.get(event=self.event, slug=pc_slug)
            Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_is_default,
                ),
            )

            Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=f"Näkymätön {role_title.lower()}",
                defaults=dict(
                    override_public_title=role_title,
                    is_default=False,
                    is_public=False,
                ),
            )

        have_categories = Category.objects.filter(event=self.event).exists()
        if not have_categories:
            for title, style in [
                ("Puheohjelma", "color2"),
                ("Miitti", "miitti"),
                ("Työpaja", "color3"),
                ("Muu ohjelma", "muu"),
            ]:
                Category.objects.get_or_create(
                    event=self.event,
                    style=style,
                    defaults=dict(
                        title=title,
                    ),
                )

        for start_time, end_time in [
            (
                self.event.start_time.replace(hour=10, minute=0, tzinfo=self.tz),
                self.event.start_time.replace(hour=20, minute=0, tzinfo=self.tz),
            ),
            (
                self.event.end_time.replace(hour=10, minute=0, tzinfo=self.tz),
                self.event.end_time.replace(hour=20, minute=0, tzinfo=self.tz),
            ),
        ]:
            TimeBlock.objects.get_or_create(
                event=self.event,
                start_time=start_time,
                defaults=dict(end_time=end_time),
            )

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Quarter hours
            # [:-1] – discard 18:00 to 19:00
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                # for minute in [15, 30, 45]:
                for minute in [30]:
                    SpecialStartTime.objects.get_or_create(
                        event=self.event,
                        start_time=hour_start_time.replace(minute=minute),
                    )

        for tag_title, tag_class in [
            ("Suositeltu", "hilight"),
            ("Musiikki", "label-info"),
            ("In English", "label-success"),
            ("English OK", "label-success"),
            ("K-18", "label-danger"),
            ("Paikkaliput", "label-default"),
            ("Kirkkaita/välkkyviä valoja", "label-warning"),
            ("Kovia ääniä", "label-warning"),
            ("Savutehosteita", "label-warning"),
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                title=tag_title,
                defaults=dict(
                    style=tag_class,
                ),
            )

        default_form, created = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="default",
            defaults=dict(
                title="Tarjoa puhe- tai muuta ohjelmaa",
                short_description="Valitse tämä vaihtoehto, mikäli ohjelmanumerosi ei ole pöytäroolipeli.",
                programme_form_code="events.shumicon2023.forms:ProgrammeForm",
                num_extra_invites=3,
                order=30,
            ),
        )
        if default_form.programme_form_code == "programme.forms:ProgrammeOfferForm":
            default_form.programme_form_code = "events.shumicon2023.forms:ProgrammeForm"
            default_form.save()

        self.event.programme_event_meta.create_groups()

    def setup_intra(self):
        from intra.models import IntraEventMeta, Team

        (admin_group,) = IntraEventMeta.get_or_create_groups(self.event, ["admins"])
        organizer_group = self.event.labour_event_meta.get_group("vastaava")
        meta, unused = IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            ),
        )

        for team_slug, team_name in [
            ("infra", "Infra"),
            ("ohjelma", "Ohjelma"),
            ("palvelut", "Palvelut"),
        ]:
            (team_group,) = IntraEventMeta.get_or_create_groups(self.event, [team_slug])

            team, created = Team.objects.get_or_create(
                event=self.event,
                slug=team_slug,
                defaults=dict(
                    name=team_name,
                    order=self.get_ordering_number(),
                    group=team_group,
                ),
            )

        for team in Team.objects.filter(event=self.event):
            team.is_public = team.slug != "tracoff"
            team.save()

    def setup_directory(self):
        from directory.models import DirectoryAccessGroup

        labour_admin_group = self.event.labour_event_meta.get_group("admins")

        DirectoryAccessGroup.objects.get_or_create(
            organization=self.event.organization,
            group=labour_admin_group,
            active_from=now(),
            active_until=self.event.end_time + timedelta(days=30),
        )

    def handle(self, *args, **opts):
        self.setup_core()

class Command(BaseCommand):
    args = ""
    help = "Setup shumicon2023 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
