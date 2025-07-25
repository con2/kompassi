from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from kompassi.core.utils import full_hours_between


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
        # self.setup_access()
        self.setup_badges()
        self.setup_intra()

    def setup_core(self):
        from kompassi.core.models import Event, Organization, Venue

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
            slug="frostbite2019",
            defaults=dict(
                name="Desucon Frostbite (2019)",
                name_genitive="Desucon Frostbiten",
                name_illative="Desucon Frostbiteen",
                name_inessive="Desucon Frostbitessä",
                homepage_url="https://desucon.fi/frostbite2019/",
                organization=self.organization,
                start_time=datetime(2019, 2, 15, 17, 0, 0, tzinfo=self.tz),
                end_time=datetime(2019, 2, 17, 17, 0, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from kompassi.core.models import Person
        from kompassi.core.utils import slugify
        from kompassi.labour.models import (
            AlternativeSignupForm,
            JobCategory,
            LabourEventMeta,
            PersonnelClass,
            Qualification,
        )

        from ...models import SignupExtra, SpecialDiet

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2019, 2, 15, 8, 0, tzinfo=self.tz),
            work_ends=datetime(2019, 2, 17, 21, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email="Desuconin työvoimavastaava <tyovoima@desucon.fi>",
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
            ("Vastaava", "vastaava", "labour"),
            ("Vuorovastaava", "vuorovastaava", "labour"),
            ("Työvoima", "tyovoima", "labour"),
            ("Ohjelmanjärjestäjä", "ohjelma", "programme"),
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

        tyovoima = PersonnelClass.objects.get(event=self.event, slug="tyovoima")
        vastaava = PersonnelClass.objects.get(event=self.event, slug="vastaava")

        for name, description, pcs in [
            ("Vastaava", "Tapahtuman järjestelytoimikunnan jäsen eli vastaava", [vastaava]),
            (
                "Järjestyksenvalvoja",
                "Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa "
                "JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole "
                "täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).",
                [tyovoima],
            ),
        ]:
            job_category, created = JobCategory.objects.get_or_create(
                event=self.event,
                slug=slugify(name),
                defaults=dict(
                    name=name,
                    description=description,
                ),
            )

            if created:
                job_category.personnel_classes.set(pcs)

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
                signup_form_class_path="events.frostbite2019.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.frostbite2019.forms:OrganizerSignupExtraForm",
                active_from=datetime(2018, 9, 16, 0, 0, 0, tzinfo=self.tz),
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

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="xxlomake",
            defaults=dict(
                title="Erikoistehtävien ilmoittautumislomake",
                signup_form_class_path="events.frostbite2019.forms:SpecialistSignupForm",
                signup_extra_form_class_path="events.frostbite2019.forms:SpecialistSignupExtraForm",
                active_from=datetime(2018, 9, 16, 0, 0, 0, tzinfo=self.tz),
                active_until=self.event.start_time,
                signup_message=(
                    "Täytä tämä lomake vain, "
                    "jos joku Desuconin vastaavista on ohjeistanut sinun ilmoittautua tällä lomakkeella. "
                ),
            ),
        )

        # Survey.objects.get_or_create(
        #     event=self.event,
        #     slug='kaatoilmo',
        #     defaults=dict(
        #         title='Ilmoittautuminen kaatajaisiin',
        #         description=(
        #             'Voidaksemme ilmoittaa erikoisruokavaliot mahdollisimman tarkasti pitopalvelulle '
        #             'pyydämme ilmoittamaan, aiotko osallistua kaatajaisiin Desuconin purun jälkeen '
        #             'sunnuntaina 10. kesäkuuta 2019 noin kello 19:00.'
        #         ),
        #         form_class_path='events.frostbite2019.forms:AfterpartyParticipationSurvey',
        #         active_from=datetime(2019, 6, 2, 21, 34, 0, tzinfo=self.tz),
        #         active_until=datetime(2019, 6, 10, 23, 59, 59, tzinfo=self.tz),
        #     ),
        # )

    def setup_badges(self):
        from kompassi.badges.models import BadgesEventMeta

        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                real_name_must_be_visible=True,
            ),
        )

    def setup_programme(self):
        from kompassi.labour.models import PersonnelClass
        from kompassi.zombies.programme.models import (
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

        role_priority = 0
        for role_title in [
            "Ohjelmanjärjestäjä",
            "Panelisti",
            "Työpajanpitäjä",
            "Keskustelupiirin vetäjä",
        ]:
            role, unused = Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=True,
                    require_contact_info=True,
                    priority=role_priority,
                ),
            )
            role_priority += 10

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
            Category.objects.get_or_create(
                event=self.event,
                slug=slug,
                defaults=dict(
                    title=title,
                    style=style,
                    public=style != "sisainen",
                ),
            )

        form, created = AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug="default",
            defaults=dict(
                title="Ohjelmalomake",
                short_description="",
                programme_form_code="events.frostbite2019.forms:ProgrammeForm",
                num_extra_invites=0,
            ),
        )

        if not TimeBlock.objects.filter(event=self.event).exists():
            for start_time, end_time in [
                (
                    datetime(2019, 2, 15, 17, 0, 0, tzinfo=self.tz),
                    datetime(2019, 2, 16, 1, 0, 0, tzinfo=self.tz),
                ),
                (
                    datetime(2019, 2, 16, 9, 0, 0, tzinfo=self.tz),
                    datetime(2019, 2, 17, 1, 0, 0, tzinfo=self.tz),
                ),
                (
                    datetime(2019, 2, 17, 9, 0, 0, tzinfo=self.tz),
                    datetime(2019, 2, 17, 18, 0, 0, tzinfo=self.tz),
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

    def setup_access(self):
        from kompassi.access.models import GroupPrivilege, Privilege

        # Grant accepted workers and programme hosts access to Desucon Slack
        privilege = Privilege.objects.get(slug="desuslack")
        for group in [
            self.event.labour_event_meta.get_group("accepted"),
            # self.event.programme_event_meta.get_group("hosts"),
        ]:
            GroupPrivilege.objects.get_or_create(group=group, privilege=privilege, defaults=dict(event=self.event))

    def setup_intra(self):
        from kompassi.intra.models import IntraEventMeta, Team

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
    help = "Setup frostbite2019 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
