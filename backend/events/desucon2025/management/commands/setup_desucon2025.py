from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from access.models import GroupPrivilege, Privilege
from badges.models import BadgesEventMeta
from core.models import Event, Organization, Person, Venue
from intra.models import IntraEventMeta, Team
from labour.models import (
    AlternativeSignupForm,
    JobCategory,
    LabourEventMeta,
    PersonnelClass,
    Qualification,
    Survey,
)

from ...models import Poison, SignupExtra, SpecialDiet


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
            slug="desucon2025",
            defaults=dict(
                name="Desucon (2025)",
                name_genitive="Desuconin",
                name_illative="Desuconiin",
                name_inessive="Desuconissa",
                homepage_url="https://desucon.fi/desucon2025/",
                organization=self.organization,
                start_time=datetime(2025, 6, 13, 17, 0, 0, tzinfo=self.tz),
                end_time=datetime(2025, 6, 15, 17, 0, 0, tzinfo=self.tz),
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
                "2 ruokalippua, paita (tarkista paitakoko!), badge. Kasauksen ruokalippu pe ennen klo 12.",
            ),
            (
                "Ohjelmanjärjestäjä (2. lk)",
                "ohjelma-2lk",
                "programme",
                "1 ruokalippu, badge. (Ei paitaa!) Kasauksen ruokalippu pe ennen klo 12.",
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
                signup_form_class_path="events.desucon2025.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.desucon2025.forms:OrganizerSignupExtraForm",
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
                signup_form_class_path="events.desucon2025.forms:SpecialistSignupForm",
                signup_extra_form_class_path="events.desucon2025.forms:SpecialistSignupExtraForm",
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
                form_class_path="events.desucon2025.forms:AfterpartyParticipationSurvey",
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
                form_class_path="events.desucon2025.forms:AccommodationSurvey",
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
                emperkelator_name="simple",
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


class Command(BaseCommand):
    args = ""
    help = "Setup desucon2025 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
