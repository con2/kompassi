import logging
import os
from datetime import datetime, timedelta

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

logger = logging.getLogger(__name__)


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
        self.setup_tickets_v2()
        self.setup_intra()
        self.setup_forms()

    def setup_core(self):
        from kompassi.core.models import Event, Organization, Venue

        self.venue, _ = Venue.objects.get_or_create(
            name="SeAMK Frami F",
            defaults=dict(
                name_inessive="SeAMK Frami F:llä",
            ),
        )
        self.organization, _ = Organization.objects.get_or_create(
            slug="cosmocon-ry",
            defaults=dict(
                name="Cosmocon ry",
                homepage_url="https://cosmocon.fi/",
            ),
        )
        self.event, _ = Event.objects.get_or_create(
            slug="cosmocon2026",
            defaults=dict(
                name="Cosmocon 2026",
                name_genitive="Cosmoconin",
                name_illative="Cosmoconiin",
                name_inessive="Cosmoconissa",
                homepage_url="https://cosmocon.fi",
                organization=self.organization,
                start_time=datetime(2026, 2, 21, 11, 0, tzinfo=self.tz),
                end_time=datetime(2026, 2, 22, 17, 0, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_labour(self):
        from django.contrib.contenttypes.models import ContentType

        from kompassi.core.models import Person
        from kompassi.labour.models import LabourEventMeta
        from kompassi.labour.models.job_category import JobCategory
        from kompassi.labour.models.personnel_class import PersonnelClass

        from ...models import SignupExtra

        (labour_admin_group,) = LabourEventMeta.get_or_create_groups(self.event, ["admins"])

        if self.test:
            from kompassi.core.models import Person

            person, _ = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)  # type: ignore

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=self.event.start_time - timedelta(days=1),
            work_ends=self.event.end_time + timedelta(hours=4),
            registration_opens=datetime(2025, 10, 21, 0, 0, tzinfo=self.tz),
            registration_closes=self.event.start_time,
            admin_group=labour_admin_group,
            contact_email="Cosmoconin työvoimavastaava <talkoo@cosmocon.fi>",
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )

        labour_event_meta, _ = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        ## Organizers PersonnelClass
        organizers_personnel_class, _ = PersonnelClass.objects.get_or_create(
            event=self.event,
            slug="organizers",
            defaults=dict(
                name="Vastaavat",
                app_label="labour",
                priority=self.get_ordering_number(),
            ),
        )

        ## Cosmocon työryhmä JobCategory
        ctora_job_category, created = JobCategory.objects.get_or_create(
            event=self.event,
            slug="ctora",
            defaults=dict(
                name="Cosmocon työryhmä",
                description="Tapahtuman suunnittelusta ja valmistelusta vastaavan järjestelytyöryhmän jäsen",
                public=True,
            ),
        )
        if created:
            ctora_job_category.personnel_classes.set([organizers_personnel_class])

        labour_event_meta.create_groups()

    def setup_tickets_v2(self):
        from kompassi.tickets_v2.models.meta import TicketsV2EventMeta
        from kompassi.tickets_v2.optimized_server.models.enums import PaymentProvider

        (admin_group,) = TicketsV2EventMeta.get_or_create_groups(self.event, ["admins"])
        meta, _ = TicketsV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                contact_email="Cosmocon 2026 <info@cosmocon.fi>",
                provider_id=PaymentProvider.PAYTRAIL.value,
                terms_and_conditions_url_fi="https://cosmocon.fi/liput/toimitusehdot/",
            ),
        )
        meta.ensure_partitions()

    def setup_intra(self):
        from kompassi.intra.models import IntraEventMeta

        (admin_group,) = IntraEventMeta.get_or_create_groups(self.event, ["admins"])
        organizer_group = self.event.labour_event_meta.get_group("ctora")
        meta, _ = IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            ),
        )

    def setup_forms(self):
        from kompassi.forms.models.meta import FormsEventMeta

        (admin_group,) = FormsEventMeta.get_or_create_groups(self.event, ["admins"])
        FormsEventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
            ),
        )


class Command(BaseCommand):
    args = ""
    help = "Setup Cosmocon2026 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
