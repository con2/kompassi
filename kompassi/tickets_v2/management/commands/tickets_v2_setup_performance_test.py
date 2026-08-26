"""
Seeds a synthetic `perftest` event whose quotas and products mirror the shape of the
real tracon2026 on-sale (2026-07-12), so the load generator (tickets_v2_emloaden) offers
realistic contention. See docs/tickets-v2-load-testing.md for the derivation of these
numbers from the production dump.

Deliberately does not touch any real event: unlike the old version of this command,
which called setup_tracon2025 --dev-tickets, this creates its own Event/Organization/
Venue so the seeder can never mutate production data mounted into the local `postgres`
service.
"""

import logging
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.utils.timezone import now

from kompassi.core.models.event import Event
from kompassi.core.models.organization import Organization
from kompassi.core.models.venue import Venue
from kompassi.tickets_v2.models.meta import TicketsV2EventMeta
from kompassi.tickets_v2.models.product import Product
from kompassi.tickets_v2.models.quota import Quota
from kompassi.tickets_v2.optimized_server.models.enums import PaymentProvider

logger = logging.getLogger(__name__)

EVENT_SLUG = "perftest"

# Quota sizes and the products/quotas shape mirror the measured tracon2026 on-sale.
# See "The performance expectation, from the real sale" in docs/tickets-v2-load-testing.md.
QUOTAS = {
    "Perjantai": 5300,
    "Lauantai": 5300,
    "Sunnuntai": 5300,
    "Iltabileet": 1000,
}


class NotReally(Exception):
    pass


class Command(BaseCommand):
    help = "Seed a synthetic perftest event for tickets_v2 load testing"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("--really", default=False, action="store_true")
        parser.add_argument(
            "--quota-scale",
            type=float,
            default=1.0,
            help="Scale factor applied to all quota sizes, for faster iteration on the harness itself.",
        )

    def handle(self, *args, **opts):
        if not opts["really"]:
            raise NotReally(
                "Use --really to actually seed the database. You probably shouldn't do this in production :))"
            )

        quota_scale = opts["quota_scale"]

        with transaction.atomic():
            organization, _unused = Organization.objects.get_or_create(
                slug="perftest",
                defaults=dict(
                    name="Perftest",
                    name_genitive="Perftestin",
                ),
            )
            venue, _unused = Venue.objects.get_or_create(
                name="Perftest Venue",
                defaults=dict(name_inessive="Perftest Venuessa"),
            )
            event, _unused = Event.objects.get_or_create(
                slug=EVENT_SLUG,
                defaults=dict(
                    name="Perftest",
                    name_genitive="Perftestin",
                    name_illative="Perftestiin",
                    name_inessive="Perftestissä",
                    organization=organization,
                    venue=venue,
                ),
            )

            (admin_group,) = TicketsV2EventMeta.get_or_create_groups(event, ["admins"])
            meta, _unused = TicketsV2EventMeta.objects.update_or_create(
                event=event,
                defaults=dict(
                    admin_group=admin_group,
                    provider=PaymentProvider.NONE,
                ),
            )
            meta.ensure_partitions()

            available_from = now()
            available_until = available_from + timedelta(days=1)

            quotas: dict[str, Quota] = {}
            for name, size in QUOTAS.items():
                quota, _unused = Quota.objects.get_or_create(event=event, name=name)
                quota.set_quota(round(size * quota_scale))
                quotas[name] = quota

            for name in ("Perjantai", "Lauantai", "Sunnuntai"):
                quotas[name].products.get_or_create(
                    event=event,
                    title=f"Perftest - {name}lippu",
                    defaults=dict(
                        price=Decimal("0.00"),
                        available_from=available_from,
                        available_until=available_until,
                    ),
                )

            quotas["Iltabileet"].products.get_or_create(
                event=event,
                title="Perftest - Iltabileet",
                defaults=dict(
                    price=Decimal("0.00"),
                    available_from=available_from,
                    available_until=available_until,
                ),
            )

            weekend_product, created = Product.objects.get_or_create(
                event=event,
                title="Perftest - Viikonloppulippu",
                defaults=dict(
                    price=Decimal("0.00"),
                    available_from=available_from,
                    available_until=available_until,
                ),
            )
            if created:
                weekend_product.quotas.set([quotas["Perjantai"], quotas["Lauantai"], quotas["Sunnuntai"]])

        logger.info("Seeded perftest event with quota_scale=%s", quota_scale)
