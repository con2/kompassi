import logging
from collections import Counter

from django.core.management.base import BaseCommand

from core.models import Event

from ...models.order import Order
from ...models.product import Product
from ...models.quota import Quota
from ...optimized_server.models.quota import get_quota_ids_by_product_id_django

logger = logging.getLogger("kompassi")


class Command(BaseCommand):
    args = "[event_slug...]"
    help = "Check that all orders are assigned the correct amount of tickets"

    def add_arguments(self, parser):
        parser.add_argument(
            "event_slugs",
            nargs="+",
            metavar="EVENT_SLUG",
        )

    def handle(*args, **opts):
        have_conflicts = False

        for event_slug in opts["event_slugs"]:
            total_by_product_id: Counter[int] = Counter()
            total_by_quota_id: Counter[int] = Counter()

            event = Event.objects.get(slug=event_slug)
            quota_ids_by_product_id = get_quota_ids_by_product_id_django(event.id)

            for order in Order.objects.filter(event=event):
                expected_quantities_by_quota_id: Counter[int] = Counter()
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

        if have_conflicts:
            raise AssertionError("Conflicts found.")
