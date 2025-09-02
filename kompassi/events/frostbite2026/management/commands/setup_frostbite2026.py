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
from kompassi.badges.models.survey_to_badge import SurveyToBadgeMapping
from kompassi.core.models.event import Event
from kompassi.core.models.organization import Organization
from kompassi.core.models.person import Person
from kompassi.core.models.venue import Venue
from kompassi.core.utils.log_utils import log_get_or_create
from kompassi.forms.models.meta import FormsEventMeta
from kompassi.forms.models.survey import Survey
from kompassi.intra.models import IntraEventMeta, Team
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
        self.setup_access()
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
            slug="frostbite2026",
            defaults=dict(
                name="Desucon Frostbite (2026)",
                name_genitive="Desucon Frostbiten",
                name_illative="Desucon Frostbiteen",
                name_inessive="Desucon Frostbitessä",
                homepage_url="https://desucon.fi/frostbite2026/",
                organization=self.organization,
                start_time=datetime(2026, 1, 23, 17, 0, 0, tzinfo=self.tz),
                end_time=datetime(2026, 1, 25, 17, 0, 0, tzinfo=self.tz),
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

        for pc_name, pc_slug, pc_app_label, pc_perks in [
            (
                "Vastaava",
                "vastaava",
                "labour",
                "3 ruokalippua, paita (tarkista paitakoko!), badge",
            ),
            (
                "Vuorovastaava",
                "vuorovastaava",
                "labour",
                "2 ruokalippua, paita (tarkista paitakoko!), badge. Kasauksen ruokalippu pe ennen klo 12.",
            ),
            (
                "Työvoima",
                "tyovoima",
                "labour",
                "2 ruokalippua, paita (tarkista paitakoko!), badge. Kasauksen ruokalippu pe ennen klo 12.",
            ),
            (
                "Ohjelmanjärjestäjä",
                "ohjelma",
                "programme",
                "Määräytyy ohjelmatyypin perusteella (SINUN EI PITÄISI NÄHDÄ TÄTÄ TEKSTIÄ!)",
            ),
            (
                "Ohjelmanjärjestäjä (2. lk)",
                "ohjelma-2lk",
                "programme",
                "Määräytyy ohjelmatyypin perusteella (SINUN EI PITÄISI NÄHDÄ TÄTÄ TEKSTIÄ!)",
            ),
            ("Guest of Honour", "goh", "programme", "Badge"),
            ("Media", "media", "badges", "Badge"),
            ("Myyjä", "myyja", "badges", ""),
            ("Vieras", "vieras", "badges", ""),
        ]:
            personnel_class, created = PersonnelClass.objects.update_or_create(
                event=self.event,
                slug=pc_slug,
                defaults=dict(
                    name=pc_name,
                    app_label=pc_app_label,
                    priority=self.get_ordering_number(),
                    override_formatted_perks=pc_perks,
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
                signup_form_class_path="events.frostbite2026.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.frostbite2026.forms:OrganizerSignupExtraForm",
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
                signup_form_class_path="events.frostbite2026.forms:SpecialistSignupForm",
                signup_extra_form_class_path="events.frostbite2026.forms:SpecialistSignupExtraForm",
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
                form_class_path="events.frostbite2026.forms:AfterpartyParticipationSurvey",
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
                form_class_path="events.frostbite2026.forms:AccommodationSurvey",
                active_from=now(),
                active_until=self.event.start_time,
            ),
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

    def setup_access(self):
        # Grant accepted workers and programme hosts access to Desucon Slack
        privilege = Privilege.objects.get(slug="desuslack")
        for group in [
            self.event.labour_event_meta.get_group("accepted"),
            # self.event.programme_event_meta.get_group("hosts"),
        ]:
            GroupPrivilege.objects.get_or_create(group=group, privilege=privilege, defaults=dict(event=self.event))

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

        survey = Survey.objects.filter(event=self.event, slug="program-host-signup").first()
        if survey:
            ohjelma = PersonnelClass.objects.get(event=self.event, slug="ohjelma")

            SurveyToBadgeMapping.objects.filter(required_dimensions={}).delete()
            for value_slug, job_title, perks in [
                (
                    "ohjelmanpitaja",
                    "Ohjelmanjärjestäjä",
                    "2 ruokalippua, paita (tarkista paitakoko!), badge. Kasauksen ruokalippu pe ennen klo 12.",
                ),
                (
                    "muu",
                    "Ohjelmanjärjestäjä",
                    "2 ruokalippua, paita (tarkista paitakoko!), badge. Kasauksen ruokalippu pe ennen klo 12.",
                ),
                (
                    "visaohjelma",
                    "Ohjelmanjärjestäjä",
                    "2 ruokalippu, paita (tarkista paitakoko!), badge. Kasauksen ruokalippu pe ennen klo 12.",
                ),
                (
                    "panelisti",
                    "Ohjelmanjärjestäjä",
                    "1 ruokalippu, paita (tarkista paitakoko!), badge. Kasauksen ruokalippu pe ennen klo 12.",
                ),
                (
                    "piirinvetaja",
                    "Ohjelmanjärjestäjä",
                    "1 ruokalippu, paita (tarkista paitakoko!), badge. Kasauksen ruokalippu pe ennen klo 12.",
                ),
                (
                    "pajanpitaja",
                    "Ohjelmanjärjestäjä",
                    "1 ruokalippu, paita (tarkista paitakoko!), badge. Kasauksen ruokalippu pe ennen klo 12.",
                ),
                (
                    "esiintyja",
                    "Esiintyjä",
                    "1 ruokalippu, paita (tarkista paitakoko!), badge. Kasauksen ruokalippu pe ennen klo 12.",
                ),
                (
                    "tuomari",
                    "Tuomari",
                    "1 ruokalippu, paita (tarkista paitakoko!), badge. Kasauksen ruokalippu pe ennen klo 12.",
                ),
                (
                    "juontaja",
                    "Juontaja",
                    "1 ruokalippu, paita (tarkista paitakoko!), badge. Kasauksen ruokalippu pe ennen klo 12.",
                ),
            ]:
                SurveyToBadgeMapping.objects.update_or_create(
                    survey=survey,
                    required_dimensions={"personnel-class": [value_slug]},
                    personnel_class=ohjelma,
                    defaults=dict(
                        job_title=job_title,
                        priority=self.get_ordering_number(),
                        annotations={"frostbite2026:formattedPerks": perks},
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

        ohjelma = PersonnelClass.objects.get(event=self.event, slug="ohjelma")
        InvolvementToBadgeMapping.objects.update_or_create(
            universe=universe,
            personnel_class=ohjelma,
            defaults=dict(
                required_dimensions={
                    "state": ["active"],
                    "type": ["combined-perks"],
                    "v1-personnel-class": ["ohjelma"],
                },
                job_title="Ohjelmanpitäjä",
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


class Command(BaseCommand):
    args = ""
    help = "Setup frostbite2026 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
