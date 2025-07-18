from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.utils import full_hours_between


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
        # self.setup_programme()
        self.setup_access()
        self.setup_badges()
        self.setup_intra()

    def setup_core(self):
        from core.models import Event, Organization, Venue

        self.venue, unused = Venue.objects.get_or_create(
            name="Lahden Sibeliustalo",
            defaults=dict(
                name_inessive="Lahden Sibeliustalolla",  # not really inessive though
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="kehittyvien-conien-suomi-ry",
            defaults=dict(
                name="Kehittyvien conien Suomi ry",
                homepage_url="https://desucon.fi/kcs/",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="desucon2024",
            defaults=dict(
                name="Desucon (2024)",
                name_genitive="Desuconin",
                name_illative="Desuconiin",
                name_inessive="Desuconissa",
                homepage_url="https://desucon.fi/desucon2024/",
                organization=self.organization,
                start_time=datetime(2024, 6, 14, 17, 0, 0, tzinfo=self.tz),
                end_time=datetime(2024, 6, 16, 17, 0, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from core.models import Event, Person
        from labour.models import (
            AlternativeSignupForm,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Qualification,
            Survey,
        )

        from ...models import Poison, SignupExtra, SpecialDiet

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)  # type: ignore

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time.replace(hour=8, minute=0, tzinfo=self.tz),
            work_ends=self.event.end_time.replace(hour=21, minute=0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email="Desuconin työvoimavastaava <tyovoima@desucon.fi>",
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),  # type: ignore
                registration_closes=t + timedelta(days=60),  # type: ignore
            )

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            ("Vastaava", "vastaava", "labour"),
            ("Vuorovastaava", "vuorovastaava", "labour"),
            ("Työvoima", "tyovoima", "labour"),
            ("Ohjelmanjärjestäjä", "ohjelma", "programme"),
            ("Ohjelmanjärjestäjä (2. lk)", "ohjelma-2lk", "programme"),
            ("Guest of Honour", "goh", "programme"),
            ("Media", "media", "badges"),
            ("Myyjä", "myyja", "badges"),
            ("Vieras", "vieras", "badges"),
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
                source_event=Event.objects.get(slug="frostbite2024"),
                target_event=self.event,
            )

        for name in ["Vastaava"]:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ("Järjestyksenvalvoja", "JV-kortti"),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

            jc.required_qualifications.set([qual])

        labour_event_meta.create_groups()

        organizer_form, unused = AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="vastaava",
            defaults=dict(
                title="Vastaavan ilmoittautumislomake",
                signup_form_class_path="events.desucon2024.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.desucon2024.forms:OrganizerSignupExtraForm",
                active_from=self.event.created_at,
                active_until=self.event.start_time,
            ),
        )

        if organizer_form.active_until is None:
            organizer_form.active_until = self.event.start_time
            organizer_form.save()

        for diet_name in [
            "Gluteeniton",
            "Laktoositon",
            "Maidoton",
            "Vegaaninen",
            "Lakto-ovo-vegetaristinen",
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        for poison in [
            "Olut",
            "Olut (gluteeniton)",
            "Siideri",
            "Lonkero",
            "Limu (sokerillinen)",
            "Limu (sokeriton)",
        ]:
            Poison.objects.get_or_create(name=poison)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="xxlomake",
            defaults=dict(
                title="Erikoistehtävien ilmoittautumislomake",
                signup_form_class_path="events.desucon2024.forms:SpecialistSignupForm",
                signup_extra_form_class_path="events.desucon2024.forms:SpecialistSignupExtraForm",
                active_from=self.event.created_at,
                active_until=self.event.start_time,
                signup_message=(
                    "Täytä tämä lomake vain, "
                    "jos joku Desuconin vastaavista on ohjeistanut sinun ilmoittautua tällä lomakkeella. "
                ),
            ),
        )

        Survey.objects.get_or_create(
            event=self.event,
            slug="kaatoilmo",
            defaults=dict(
                title="Ilmoittautuminen kaatajaisiin",
                description=(
                    "Voidaksemme ilmoittaa erikoisruokavaliot mahdollisimman tarkasti pitopalvelulle "
                    "pyydämme ilmoittamaan, aiotko osallistua kaatajaisiin Desuconin purun jälkeen "
                    "tapahtumaviikonlopun sunnuntaina noin kello 19."
                ),
                form_class_path="events.desucon2024.forms:AfterpartyParticipationSurvey",
                active_from=now(),
                active_until=self.event.start_time,
            ),
        )

        Survey.objects.get_or_create(
            event=self.event,
            slug="tyovoimamajoitus",
            defaults=dict(
                title="Ilmoittautuminen työvoimamajoitukseen",
                description=(
                    "Tarjoamme työvoimalle ja ohjelmanjärjestäjille tarvittaessa maksuttoman lattiamajoituksen Kuusi-salissa "
                    "tapahtuman molempina öinä. Majoitustilan riittävyyden arvioimiseksi pyydämme ilmoittamaan, "
                    "tarvitsetko majoitusta ja mille öille."
                ),
                form_class_path="events.desucon2024.forms:AccommodationSurvey",
                active_from=now(),
                active_until=self.event.start_time,
            ),
        )

    def setup_badges(self):
        from badges.models import BadgesEventMeta

        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                real_name_must_be_visible=True,
            ),
        )

    def setup_programme(self):
        from labour.models import PersonnelClass
        from programme.models import (
            AlternativeProgrammeForm,
            Category,
            ProgrammeEventMeta,
            Role,
            Room,
            SpecialStartTime,
            Tag,
            TimeBlock,
            View,
        )

        ProgrammeEventMeta.get_or_create_groups(self.event, ["hosts"])
        (programme_admin_group,) = ProgrammeEventMeta.get_or_create_groups(self.event, ["admins"])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                public=False,
                admin_group=programme_admin_group,
                contact_email="Desuconin ohjelmavastaava <ohjelma@desucon.fi>",
            ),
        )

        personnel_class = PersonnelClass.objects.get(event=self.event, slug="ohjelma")
        personnel_2nd_class = PersonnelClass.objects.get(event=self.event, slug="ohjelma-2lk")

        role_priority = 0
        for role_title in [
            "Ohjelmanjärjestäjä",
            "Näkymätön ohjelmanjärjestäjä",
            "Panelisti",
            "Työpajanpitäjä",
            "Keskustelupiirin vetäjä",
            "Tuomari",
            "Juontaja",
        ]:
            role_personnel_class = personnel_class if "hjelmanjärjestäjä" in role_title else personnel_2nd_class

            role, unused = Role.objects.get_or_create(
                title=role_title,
                personnel_class__event=self.event,
                defaults=dict(
                    personnel_class=role_personnel_class,
                    is_default=role_title == "Ohjelmanjärjestäjä",
                    is_public=role_title not in ["Näkymätön ohjelmanjärjestäjä", "Tuomari"],
                    require_contact_info=True,
                    priority=role_priority,
                ),
            )
            role_priority += 10

            # remove for frostbite2024
            if role.personnel_class != role_personnel_class:
                role.personnel_class = role_personnel_class
                role.save()

        Role.objects.filter(
            personnel_class__event=self.event,
            title="Näkymätön ohjelmanjärjestäjä",
            override_public_title="",
        ).update(
            override_public_title="Ohjelmanjärjestäjä",
        )

        for title, slug, style in [
            ("Muu ohjelma", "other", "color1"),
            ("Paneeli", "paneeli", "color2"),
            ("Luento", "luento", "color3"),
            ("Keskustelupiiri", "keskustelupiiri", "color4"),
            ("Paja", "paja", "color5"),
            ("Pienluento", "pienluento", "color6"),
            ("Esitys", "esit", "color7"),
            ("Visa", "visa", "color7"),
            ("Erikoisohjelma", "erik", "color7"),
            ("Sisäinen ohjelma", "sisainen-ohjelma", "sisainen"),
        ]:
            Category.objects.update_or_create(
                event=self.event,
                slug=slug,
                create_defaults=dict(
                    title=title,
                ),
                defaults=dict(
                    style=style,
                    public=style != "sisainen",
                    v2_dimensions={},  # force its update via .save
                ),
            )

        form, created = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="default",
            defaults=dict(
                title="Ohjelmalomake",
                short_description="",
                programme_form_code="events.desucon2024.forms:ProgrammeForm",
                num_extra_invites=0,
            ),
        )

        if not TimeBlock.objects.filter(event=self.event).exists():
            saturday = self.event.start_time + timedelta(days=1)
            for start_time, end_time in [
                (
                    self.event.start_time.replace(hour=17, minute=0, tzinfo=self.tz),
                    saturday.replace(hour=1, minute=0, tzinfo=self.tz),
                ),
                (
                    saturday.replace(hour=9, minute=0, tzinfo=self.tz),
                    self.event.end_time.replace(hour=1, minute=0, tzinfo=self.tz),
                ),
                (
                    self.event.end_time.replace(hour=9, minute=0, tzinfo=self.tz),
                    self.event.end_time.replace(hour=18, minute=0, tzinfo=self.tz),
                ),
            ]:
                TimeBlock.objects.get_or_create(
                    event=self.event, start_time=start_time, defaults=dict(end_time=end_time)
                )

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(
                    event=self.event,
                    start_time=hour_start_time.replace(minute=30),  # look, no tz
                )

        view, created = View.objects.get_or_create(
            event=self.event,
            name="Ohjelmakartta",
        )
        if created:
            view.rooms = [
                Room.objects.get_or_create(
                    event=self.event,
                    name=room_name,
                )[0]
                for room_name in [
                    "Pääsali",
                    "Kuusi",
                    "Puuseppä",
                    "Koivu",
                    "Honka",
                ]
            ]
            view.save()

        tag_order = 0
        for tag_title, tag_slug, tag_style in [
            ("Cosplaypainotteinen ohjelma", "cosplay", "label-danger"),
            ("Mangapainotteinen ohjelma", "manga", "label-success"),
            ("Ohjelman tarkoitus on viihdyttää", "viihde", "label-primary"),
            ("Ohjelma sisältää juonipaljastuksia", "spoilers", "label-warning"),
            ("Ohjelma keskittyy analysoivampaan lähestymistapaan", "analyysi", "label-default"),
            ("Animepainotteinen ohjelma", "anime", "label-info"),
        ]:
            Tag.objects.get_or_create(
                event=self.event,
                slug=tag_slug,
                defaults=dict(
                    title=tag_title,
                    order=tag_order,
                    style=tag_style,
                ),
            )
            tag_order += 10

        self.event.programme_event_meta.create_groups()

    def setup_access(self):
        from access.models import GroupPrivilege, Privilege

        # Grant accepted workers and programme hosts access to Desucon Slack
        privilege = Privilege.objects.get(slug="desuslack")
        for group in [
            self.event.labour_event_meta.get_group("accepted"),
            # self.event.programme_event_meta.get_group("hosts"),
        ]:
            GroupPrivilege.objects.get_or_create(group=group, privilege=privilege, defaults=dict(event=self.event))

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
            ("desucon", "Vastaavat"),
        ]:
            (team_group,) = IntraEventMeta.get_or_create_groups(self.event, [team_slug])
            email = f"{team_slug}@desucon.fi"

            team, created = Team.objects.get_or_create(
                event=self.event,
                slug=team_slug,
                defaults=dict(name=team_name, order=self.get_ordering_number(), group=team_group, email=email),
            )


class Command(BaseCommand):
    args = ""
    help = "Setup desucon2024 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
