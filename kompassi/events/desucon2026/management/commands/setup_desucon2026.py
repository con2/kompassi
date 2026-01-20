import logging
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from kompassi.access.models import GroupPrivilege, Privilege
from kompassi.badges.models.badges_event_meta import BadgesEventMeta
from kompassi.core.models.event import Event
from kompassi.core.models.organization import Organization
from kompassi.core.models.person import Person
from kompassi.core.models.venue import Venue
from kompassi.core.utils.log_utils import log_get_or_create
from kompassi.forms.models.meta import FormsEventMeta
from kompassi.intra.models import IntraEventMeta, Team
from kompassi.involvement.models.enums import JobTitleMode
from kompassi.involvement.models.involvement_to_badge import InvolvementToBadgeMapping
from kompassi.involvement.models.involvement_to_group import InvolvementToGroupMapping
from kompassi.involvement.models.meta import InvolvementEventMeta
from kompassi.involvement.models.registry import Registry
from kompassi.labour.models.alternative_signup_forms import AlternativeSignupForm
from kompassi.labour.models.job_category import JobCategory
from kompassi.labour.models.labour_event_meta import LabourEventMeta
from kompassi.labour.models.personnel_class import PersonnelClass
from kompassi.labour.models.qualifications import Qualification
from kompassi.labour.models.survey import Survey as LabourSurvey
from kompassi.program_v2.models.meta import ProgramV2EventMeta

from ...models import Poison, SignupExtra, SpecialDiet

logger = logging.getLogger(__name__)


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
        self.setup_intra()
        self.setup_forms()
        self.setup_program_v2()

    def setup_core(self):
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
            slug="desucon2026",
            defaults=dict(
                name="Desucon (2026)",
                name_genitive="Desuconin",
                name_illative="Desuconiin",
                name_inessive="Desuconissa",
                homepage_url="https://desucon.fi/desucon2026/",
                organization=self.organization,
                start_time=datetime(2026, 6, 12, 17, 0, 0, tzinfo=self.tz),
                end_time=datetime(2026, 6, 14, 17, 0, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)  # type: ignore

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time.replace(hour=8, minute=0, tzinfo=self.tz),  # type: ignore
            work_ends=self.event.end_time.replace(hour=21, minute=0, tzinfo=self.tz),  # type: ignore
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
            ("Ohjelmanjärjestäjä", "ohjelma", "program_v2"),
            ("Esiintyjä", "esiintyja", "program_v2"),
            ("Guest of Honour", "goh", "program_v2"),
            ("Media", "media", "badges"),
            ("Myyjä", "myyja", "badges"),
            ("Vieras", "vieras", "badges"),
        ]:
            PersonnelClass.objects.update_or_create(
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
                source_event=Event.objects.get(slug="frostbite2026"),
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
                signup_form_class_path="events.desucon2026.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.desucon2026.forms:OrganizerSignupExtraForm",
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
                signup_form_class_path="events.desucon2026.forms:SpecialistSignupForm",
                signup_extra_form_class_path="events.desucon2026.forms:SpecialistSignupExtraForm",
                active_from=self.event.created_at,
                active_until=self.event.start_time,
                signup_message=(
                    "Täytä tämä lomake vain, "
                    "jos joku Desuconin vastaavista on ohjeistanut sinun ilmoittautua tällä lomakkeella. "
                ),
            ),
        )

        LabourSurvey.objects.get_or_create(
            event=self.event,
            slug="kaatoilmo",
            defaults=dict(
                title="Ilmoittautuminen kaatajaisiin",
                description=(
                    "Voidaksemme ilmoittaa erikoisruokavaliot mahdollisimman tarkasti pitopalvelulle "
                    "pyydämme ilmoittamaan, aiotko osallistua kaatajaisiin Desuconin purun jälkeen "
                    "tapahtumaviikonlopun sunnuntaina noin kello 19."
                ),
                form_class_path="events.desucon2026.forms:AfterpartyParticipationSurvey",
                active_from=now(),
                active_until=self.event.start_time,
            ),
        )

        LabourSurvey.objects.get_or_create(
            event=self.event,
            slug="tyovoimamajoitus",
            defaults=dict(
                title="Ilmoittautuminen työvoimamajoitukseen",
                description=(
                    "Tarjoamme työvoimalle ja ohjelmanjärjestäjille tarvittaessa maksuttoman lattiamajoituksen Kuusi-salissa "
                    "tapahtuman molempina öinä. Majoitustilan riittävyyden arvioimiseksi pyydämme ilmoittamaan, "
                    "tarvitsetko majoitusta ja mille öille."
                ),
                form_class_path="events.desucon2026.forms:AccommodationSurvey",
                active_from=now(),
                active_until=self.event.start_time,
            ),
        )

        GroupPrivilege.objects.get_or_create(
            group=self.event.labour_event_meta.get_group("accepted"),
            privilege=Privilege.objects.get(slug="desuslack"),
            defaults=dict(event=self.event),
        )

    def setup_badges(self):
        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        meta, unused = BadgesEventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                real_name_must_be_visible=True,
            ),
        )

    def setup_intra(self):
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

    def setup_forms(self):
        (admin_group,) = FormsEventMeta.get_or_create_groups(self.event, ["admins"])

        FormsEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
            ),
        )

    def setup_program_v2(self):
        InvolvementEventMeta.ensure(self.event)

        (admin_group,) = ProgramV2EventMeta.get_or_create_groups(self.event, ["admins"])
        meta, _ = ProgramV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                contact_email="Desuconin ohjelmavastaava <ohjelma@desucon.fi>",
                default_registry=Registry.objects.get(
                    scope=self.event.organization.scope,
                    slug="volunteers",
                ),
            ),
        )
        meta.ensure()

        universe = self.event.involvement_universe

        # TODO label tuomari/esiintyjä as such in job_title
        for personnel_class_slug in ["vastaava", "vuorovastaava", "tyovoima", "ohjelma", "esiintyja"]:
            pc = PersonnelClass.objects.get(event=self.event, slug=personnel_class_slug)
            InvolvementToBadgeMapping.objects.update_or_create(
                universe=universe,
                personnel_class=pc,
                required_dimensions={
                    "state": ["active"],
                    "type": ["combined-perks"],
                    "v1-personnel-class": [personnel_class_slug],
                },
                defaults=dict(
                    job_title_mode=JobTitleMode.OVERRIDE,
                    job_title=pc.name,
                    priority=self.get_ordering_number(),
                ),
            )

        group, created = Group.objects.get_or_create(name=f"{self.event.slug}-program-hosts")
        log_get_or_create(logger, group, created)

        InvolvementToGroupMapping.objects.get_or_create(
            universe=universe,
            required_dimensions={
                "state": ["active"],
                "type": ["program-host"],
            },
            group=group,
        )

        GroupPrivilege.objects.get_or_create(
            group=group,
            privilege=Privilege.objects.get(slug="desuslack"),
            defaults=dict(event=self.event),
        )


class Command(BaseCommand):
    args = ""
    help = "Setup desucon2026 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
