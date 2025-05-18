import os
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from access.models import EmailAliasType, GroupEmailAliasGrant
from badges.models import BadgesEventMeta
from core.models import Event, Organization, Person, Venue
from forms.models.meta import FormsEventMeta
from intra.models import IntraEventMeta, Team
from involvement.models import Registry
from labour.models import (
    AlternativeSignupForm,
    JobCategory,
    LabourEventMeta,
    PersonnelClass,
)
from program_v2.models.meta import ProgramV2EventMeta
from program_v2.workflows.program_offer import ProgramOfferWorkflow
from tickets_v2.models.meta import TicketsV2EventMeta
from tickets_v2.optimized_server.models.enums import PaymentProvider

from ...models import Language, SignupExtra, SpecialDiet


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", *parts))


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
        self.setup_badges()
        self.setup_access()
        self.setup_program_v2()
        self.setup_tickets_v2()
        self.setup_forms()
        self.delete_tickets_v1()

    def setup_core(self):
        self.venue, unused = Venue.objects.get_or_create(
            name="Messukeskus",
            defaults=dict(
                name_inessive="Messukeskuksessa",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="ropecon-ry",
            defaults=dict(
                name="Ropecon ry",
                homepage_url="http://www.ropecon.fi/hallitus",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="ropecon2025",
            defaults=dict(
                name="Ropecon 2025",
                name_genitive="Ropecon 2025 -tapahtuman",
                name_illative="Ropecon 2025 -tapahtumaan",
                name_inessive="Ropecon 2025 -tapahtumassa",
                homepage_url="http://ropecon.fi",
                organization=self.organization,
                start_time=datetime(2025, 7, 25, 15, 0, tzinfo=self.tz),
                end_time=datetime(2025, 7, 27, 18, 0, tzinfo=self.tz),
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
            work_begins=(self.event.start_time - timedelta(days=2)).replace(hour=8, minute=0, tzinfo=self.tz),  # type: ignore
            work_ends=self.event.end_time.replace(hour=23, minute=0, tzinfo=self.tz),  # type: ignore
            admin_group=labour_admin_group,
            contact_email="Ropecon 2025 -vapaaehtoisvastaava <vapaaehtoiset@ropecon.fi>",
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
            ("Conitea", "conitea", "labour"),
            ("Vuorovastaava", "ylivankari", "labour"),
            ("Ylityöntekijä", "ylityovoima", "labour"),
            ("Työvoima", "tyovoima", "labour"),
            ("Ohjelmanjärjestäjä", "ohjelma", "program_v2"),
            ("Guest of Honour", "goh", "program_v2"),
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

        if not JobCategory.objects.filter(event=self.event).exists():
            JobCategory.copy_from_event(
                source_event=Event.objects.get(slug="ropecon2023"),
                target_event=self.event,
            )

        labour_event_meta.create_groups()

        for name in ["Conitea"]:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for diet_name in [
            "Gluteeniton",
            "Laktoositon",
            "Maidoton",
            "Vegaaninen",
            "Lakto-ovo-vegetaristinen",
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        for language in [
            "suomi / Finnish",
            "englanti / English",
            "ruotsi / Swedish",
            "saksa / German",
            "japani / Japanese",
            "eesti / Estonian",
        ]:
            Language.objects.get_or_create(name=language)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="conitea",
            defaults=dict(
                title="Conitean ilmoittautumislomake",
                signup_form_class_path="events.ropecon2025.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.ropecon2025.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="xxlomake",
            defaults=dict(
                title="Erikoistehtävien ilmoittautumislomake",
                signup_form_class_path="events.ropecon2025.forms:SpecialistSignupForm",
                signup_extra_form_class_path="events.ropecon2025.forms:SpecialistSignupExtraForm",
                active_from=self.event.created_at,
                active_until=self.event.start_time,
                signup_message=(
                    "Täytä tämä lomake vain, "
                    "jos joku Ropeconin vastaavista on ohjeistanut sinun ilmoittautua tällä lomakkeella."
                ),
            ),
        )

    def setup_badges(self):
        (badge_admin_group,) = BadgesEventMeta.get_or_create_groups(self.event, ["admins"])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
            ),
        )

    def setup_intra(self):
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
            ("talous", "Talous"),
            ("peliohjelma", "Peliohjelma"),
            ("ohjelma", "Puhe- ja muu ohjelma"),
            ("viestinta", "Viestintä"),
            ("tilat", "Tilat"),
            ("tekniikka", "Tekniikka"),
            ("vapaaehtoiset", "Vapaaehtoiset"),
            ("kavijapalvelut", "Kävijäpalvelut"),
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

    def setup_access(self):
        cc_group = self.event.labour_event_meta.get_group("conitea")

        for metavar in [
            "firstname.lastname",
            "nick",
        ]:
            alias_type = EmailAliasType.objects.get(domain__domain_name="ropecon.fi", metavar=metavar)
            GroupEmailAliasGrant.objects.get_or_create(
                group=cc_group,
                type=alias_type,
                defaults=dict(
                    active_until=self.event.end_time,
                ),
            )

    def setup_program_v2(self):
        (admin_group,) = ProgramV2EventMeta.get_or_create_groups(self.event, ["admins"])
        ProgramV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                contact_email="Ropecon 2025 -ohjelmatiimi <ohjelma@ropecon.fi>",
                default_registry=Registry.objects.get(
                    scope=self.organization.scope,
                    slug="volunteers",
                ),
            ),
        )

        # TODO(2026): Remove (normally setup when program universe is first accessed)
        ProgramOfferWorkflow.backfill(self.event)

    def setup_forms(self):
        (admin_group,) = FormsEventMeta.get_or_create_groups(self.event, ["admins"])
        FormsEventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
            ),
        )

    def setup_tickets_v2(self):
        (admin_group,) = TicketsV2EventMeta.get_or_create_groups(self.event, ["admins"])
        meta, _ = TicketsV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                provider_id=PaymentProvider.PAYTRAIL.value,
            ),
        )
        meta.ensure_partitions()

    def delete_tickets_v1(self):
        if self.event.tickets_event_meta is not None:
            self.event.tickets_event_meta.delete()


class Command(BaseCommand):
    args = ""
    help = "Setup ropecon2025 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
