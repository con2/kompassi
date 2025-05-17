import os
from datetime import datetime

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Event, Organization, Venue
from forms.models.meta import FormsEventMeta
from intra.models import IntraEventMeta
from program_v2.models.meta import ProgramV2EventMeta
from tickets_v2.models.meta import TicketsV2EventMeta
from tickets_v2.optimized_server.models.enums import PaymentProvider


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", *parts))


class Setup:
    def __init__(self):
        self._ordering = 0

    def setup(self, test=False):
        self.test = test
        self.tz = tzlocal()
        self.setup_core()
        self.setup_intra()
        self.setup_program_v2()
        self.setup_tickets_v2()
        self.setup_forms()

    def setup_core(self):
        self.venue, unused = Venue.objects.get_or_create(
            name="Helsinki",
            defaults=dict(
                name_inessive="Helsingissä",
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
            slug="ropecon2025etkot",
            defaults=dict(
                name="Ropecon 2025 etkot",
                name_genitive="Ropecon 2025 etkot -tapahtuman",
                name_illative="Ropecon 2025 etkot -tapahtumaan",
                name_inessive="Ropecon 2025 etkot -tapahtumassa",
                homepage_url="https://ropecon.fi/ropecon-etkoviikko/",
                organization=self.organization,
                start_time=datetime(2025, 7, 20, 12, 0, tzinfo=self.tz),
                end_time=datetime(2025, 7, 25, 15, 30, tzinfo=self.tz),
                venue=self.venue,
            ),
        )

    def setup_intra(self):
        (admin_group,) = IntraEventMeta.get_or_create_groups(self.event, ["admins"])

        meta, unused = IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(admin_group=admin_group),
        )

    def setup_program_v2(self):
        (admin_group,) = ProgramV2EventMeta.get_or_create_groups(self.event, ["admins"])
        ProgramV2EventMeta.objects.update_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
            ),
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
                provider_id=PaymentProvider.PAYTRAIL.value,
            ),
        )
        meta.ensure_partitions()


class Command(BaseCommand):
    args = ""
    help = "Setup for Ropecon etkot 2025"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
