from datetime import datetime

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Event, Organization, Venue
from tickets_v2.models.meta import TicketsV2EventMeta
from tickets_v2.optimized_server.models.enums import PaymentProvider


class Setup:
    def setup(self, test=False):
        self.test = test
        self.tz = tzlocal()
        self.setup_core()
        self.setup_tickets_v2()

    def setup_core(self):
        self.venue, unused = Venue.objects.get_or_create(
            name="Pohjankartanon koulu",
            defaults=dict(
                name_inessive="Pohjankartanon koululla",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="pohjoisten-conien-kyhaajat-ry",
            defaults=dict(
                name="Pohjoisten conien kyhääjät ry",
                homepage_url="http://matsucon.fi/pocky-ry/",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="matsucon2025",
            defaults=dict(
                name="Matsucon 2025",
                name_genitive="Matsuconin",
                name_illative="Matsuconiin",
                name_inessive="Matsuconissa",
                homepage_url="http://matsucon.fi",
                organization=self.organization,
                start_time=datetime(2025, 8, 9, 10, 0, tzinfo=self.tz),
                end_time=datetime(2025, 8, 10, 17, 0, tzinfo=self.tz),
                venue=self.venue,
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
    help = "Setup matsucon2025 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
