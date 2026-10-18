import logging
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from kompassi.access.constants import CBAC_VALID_AFTER_EVENT_DAYS
from kompassi.access.models import CBACEntry, GroupEmailAliasGrant
from kompassi.access.models.email_alias_domain import EmailAliasDomain
from kompassi.access.models.email_alias_type import EmailAliasVariant
from kompassi.core.models import Event, Organization, Person, Venue
from kompassi.forms.models.meta import FormsEventMeta
from kompassi.intra.models import IntraEventMeta
from kompassi.involvement.models import Registry
from kompassi.involvement.models.involvement_to_group import InvolvementToGroupMapping
from kompassi.labour.models import (
    AlternativeSignupForm,
    JobCategory,
    LabourEventMeta,
    PersonnelClass,
)
from kompassi.program_v2.models.meta import ProgramV2EventMeta
from kompassi.tickets_v2.models.meta import TicketsV2EventMeta
from kompassi.tickets_v2.optimized_server.models.enums import PaymentProvider

from ...models import SignupExtra

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
        self.setup_intra()
        self.setup_access()
        self.setup_program_v2()
        self.setup_tickets_v2()
        self.setup_forms()

    def setup_core(self):
        self.venue, _unused = Venue.objects.get_or_create(
            name="Quality Hotel Sveitsi (Hyvinkää)",
            defaults=dict(
                name_inessive="Quality Hotel Sveitsissä Hyvinkäällä",
            ),
        )
        self.organization, _unused = Organization.objects.get_or_create(
            slug="ropecon-ry",
            defaults=dict(
                name="Ropecon ry",
                homepage_url="https://ry.ropecon.fi",
            ),
        )
        self.event, _unused = Event.objects.get_or_create(
            slug="solmukohta2028",
            defaults=dict(
                name="Solmukohta 2028",
                name_genitive="Solmukohdan",
                name_illative="Solmukohtaan",
                name_inessive="Solmukohdassa",
                homepage_url="https://solmukohta.eu",
                organization=self.organization,
                start_time=datetime(2028, 5, 4, 15, 0, tzinfo=self.tz),
                end_time=datetime(2028, 5, 7, 15, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            person, _unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)  # type: ignore

        content_type = ContentType.objects.get_for_model(SignupExtra)

        start_time = self.event.start_time
        if not start_time:
            raise ValueError("Event start_time is not set (shouldn't happen, appease typechecker)")
        start_time = start_time.astimezone(self.tz)
        work_begins = (start_time - timedelta(days=1)).replace(hour=8, minute=0)

        end_time = self.event.end_time
        if not end_time:
            raise ValueError("Event end_time is not set (shouldn't happen, appease typechecker)")
        end_time = end_time.astimezone(self.tz)
        work_ends = (end_time + timedelta(days=1)).replace(hour=2, minute=0)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=work_begins,
            work_ends=work_ends,
            admin_group=labour_admin_group,
            contact_email="Solmukohta 2028 <main@solmukohta.eu>",
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),  # type: ignore
                registration_closes=t + timedelta(days=60),  # type: ignore
            )

        labour_event_meta, _unused = LabourEventMeta.objects.update_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        organizers_personnel_class, _unused = PersonnelClass.objects.update_or_create(
            event=self.event,
            slug="organizers",
            defaults=dict(
                name="Organizers",
                app_label="labour",
                priority=self.get_ordering_number(),
            ),
        )

        organizers_job_category, created = JobCategory.objects.get_or_create(
            event=self.event,
            slug="organizers",
            defaults=dict(
                name="Organizers",
                description="Member of the Solmukohta 2028 team",
                public=False,
            ),
        )
        if created:
            organizers_job_category.personnel_classes.set([organizers_personnel_class])

        labour_event_meta.create_groups()

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug="organizers",
            defaults=dict(
                title="Solmukohta 2028 team sign-up form",
                signup_form_class_path="events.solmukohta2028.forms:OrganizerSignupForm",
                signup_extra_form_class_path="events.solmukohta2028.forms:OrganizerSignupExtraForm",
                active_from=now(),
                active_until=self.event.end_time,
            ),
        )

    def setup_intra(self):
        (admin_group,) = IntraEventMeta.get_or_create_groups(self.event, ["admins"])
        organizer_group = self.event.labour_event_meta.get_group("organizers")
        IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            ),
        )

    def setup_access(self):
        organizer_group = self.event.labour_event_meta.get_group("organizers")
        for domain_name in ["ropecon.fi", "solmukohta.eu"]:
            GroupEmailAliasGrant.ensure(
                organizer_group,
                EmailAliasDomain.objects.get(domain_name=domain_name),
                [EmailAliasVariant.CUSTOM_FIRSTNAME_LASTNAME],
            )

        # Lets ropecon-aliases read the organizer group's members for Google Workspace account sync,
        # without granting it every group via the same API endpoint.
        User = get_user_model()
        ropecon_aliases = User.objects.filter(username="ropecon-aliases").first()
        if ropecon_aliases is None:
            logger.warning("setup_solmukohta2028.setup_access: user ropecon-aliases not found, skipping CBAC grant")
        else:
            assert self.event.end_time

            CBACEntry.grant_access(
                ropecon_aliases,
                claims=dict(
                    view="access_admin_group_members_api",
                    group_name=organizer_group.name,
                ),
                expires_at=self.event.end_time + timedelta(days=CBAC_VALID_AFTER_EVENT_DAYS),
            )

    def setup_program_v2(self):
        (admin_group,) = ProgramV2EventMeta.get_or_create_groups(self.event, ["admins"])
        meta, _ = ProgramV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                contact_email="Solmukohta 2028 <main@solmukohta.eu>",
                is_accepting_feedback=False,
                default_registry=Registry.objects.get(
                    scope=self.organization.scope,
                    slug="volunteers",
                ),
            ),
        )
        meta.ensure()

        group, _ = Group.objects.get_or_create(name=f"{self.event.slug}-program-hosts")
        InvolvementToGroupMapping.objects.get_or_create(
            universe=self.event.involvement_universe,
            required_dimensions={
                "state": ["active"],
                "type": ["program-host"],
            },
            group=group,
        )

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
                provider=PaymentProvider.PAYTRAIL,
                contact_email="Solmukohta 2028 <main@solmukohta.eu>",
            ),
        )
        meta.ensure_partitions()


class Command(BaseCommand):
    args = ""
    help = "Setup solmukohta2028 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
