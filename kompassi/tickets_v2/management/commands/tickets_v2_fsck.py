import argparse
import logging
from collections import Counter

from django.core.management.base import BaseCommand
from django.db import transaction

from kompassi.core.models import Event

from ...models.order import Order
from ...models.product import Product
from ...models.quota import Quota
from ...optimized_server.models.enums import PaymentStatus
from ...optimized_server.models.quota import get_quota_ids_by_product_id_django

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Check that all orders are assigned the correct amount of tickets"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="+",
            metavar="EVENT_SLUG",
        )

        parser.add_argument(
            "--fix",
            default=False,
            action=argparse.BooleanOptionalAction,
            help="Attempt to fix auto-fixable problems",
        )

    @classmethod
    def check_event(cls, event: Event):
        total_by_product_id: Counter[int] = Counter()
        total_by_quota_id: Counter[int] = Counter()
        have_conflicts = False

        meta = event.tickets_v2_event_meta

        if not meta:
            raise ValueError(f"Event {event.slug} does not have a tickets v2 meta object")

        quota_ids_by_product_id = get_quota_ids_by_product_id_django(event.id)

        for order in Order.objects.filter(event=event):
            expected_quantities_by_quota_id: Counter[int] = Counter()
            if order.cached_status == PaymentStatus.PAID:
                for product_id, quantity in order.product_data.items():
                    product_id = int(product_id)
                    total_by_product_id[product_id] += quantity
                    for quota_id in quota_ids_by_product_id[product_id]:
                        expected_quantities_by_quota_id[quota_id] += quantity
                        total_by_quota_id[quota_id] += quantity

            reserved_quantities_by_quota_id: Counter[int] = Counter()
            for ticket in order.tickets:
                reserved_quantities_by_quota_id[ticket.quota_id] += 1

            if reserved_quantities_by_quota_id != expected_quantities_by_quota_id:
                logger.error(
                    "Order %s has %s, expected %s",
                    order.id,
                    reserved_quantities_by_quota_id,
                    expected_quantities_by_quota_id,
                )
                have_conflicts = True

        print()
        print("Products sold:")
        for product_id, num_sold in total_by_product_id.items():
            product = Product.objects.get(id=product_id)
            print(f"  {num_sold}\t{product.title}")
        print()

        print("Tickets assigned:")
        for quota_id, num_assigned in total_by_quota_id.items():
            quota = Quota.objects.get(id=quota_id)
            print(f"  {num_assigned}\t{quota.name}")
        print()

        return have_conflicts

    @classmethod
    def handle(cls, *args, **opts):
        have_conflicts = False
        fix = opts["fix"]

        for event_slug in opts["event_slugs"]:
            event = Event.objects.get(slug=event_slug)
            event_has_conflicts = cls.check_event(event)

            if event_has_conflicts and fix:
                logger.info("Event %s has conflicts, checking if reticket will fix them", event)
                meta = event.tickets_v2_event_meta
                if not meta:
                    raise ValueError(f"Event {event.slug} does not have a tickets v2 meta object")

                with transaction.atomic():
                    meta.reticket()
                    event_has_conflicts = cls.check_event(event)

                    if event_has_conflicts:
                        raise ValueError("Conflicts remain after reticketing")

                logger.info("Reticketing fixed problems for %s", event)

            if event_has_conflicts:
                have_conflicts = True

        if have_conflicts:
            if fix:
                meta.reticket()

            raise AssertionError("Conflicts found.")
