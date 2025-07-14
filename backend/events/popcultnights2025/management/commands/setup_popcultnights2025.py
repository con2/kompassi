import os
from datetime import datetime

from dateutil.tz import tzlocal
from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import Event, Organization, Venue
from tickets_v2.models.meta import TicketsV2EventMeta
from tickets_v2.optimized_server.models.enums import PaymentProvider


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
        self.setup_tickets_v2()

    def setup_core(self):
        self.venue, unused = Venue.objects.get_or_create(
            name="Tiivistämö",
            defaults=dict(
                name_inessive="Tiivistämöllä",
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug="finnish-fandom-conventions-ry",
            defaults=dict(
                name="Finnish Fandom Conventions ry",
                homepage_url="http://popcult.fi",
            ),
        )
        self.event, unused = Event.objects.get_or_create(
            slug="popcultnights2025",
            defaults=dict(
                name="Popcult Nights (2025)",
                name_genitive="Popcult Nightsin",
                name_illative="Popcult Nightsiin",
                name_inessive="Popcult Nightsissä",
                homepage_url="https://popcult.fi/nights-2025/",
                organization=self.organization,
                start_time=datetime(2025, 10, 4, 19, 0, tzinfo=self.tz),
                end_time=datetime(2025, 10, 4, 23, 59, 59, tzinfo=self.tz),
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
                # terms_and_conditions_url_en="",
                # terms_and_conditions_url_fi="",
            ),
        )

        meta.ensure_partitions()


class Command(BaseCommand):
    args = ""
    help = "Setup popcultnights2025 specific stuff"

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
