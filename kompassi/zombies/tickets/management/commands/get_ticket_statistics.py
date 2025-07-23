import csv
from collections import Counter, defaultdict
from sys import stdout

from django.core.management import BaseCommand

from kompassi.core.models import Event

from ...models import OrderProduct, Product


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("event_strs", nargs="+", metavar="EVENT_SLUG:PRODUCT_ID,PRODUCT_ID...")

    def handle(self, *args, **options):
        stats = defaultdict(Counter)

        event_slugs = []

        for event_str in options["event_strs"]:
            event_slug, product_ids = event_str.split(":", 1)
            event_slugs.append(event_slug)

            event = Event.objects.get(slug=event_slug)

            product_ids = [int(i) for i in product_ids.split(",")]
            products = Product.objects.filter(event__slug=event_slug, id__in=product_ids)

            for op in OrderProduct.objects.filter(
                product__in=products,
                order__confirm_time__isnull=False,
                order__payment_date__isnull=False,
                order__cancellation_time__isnull=True,
            ).distinct():
                days_to_event = (event.start_time - op.order.confirm_time).days
                stats[-days_to_event][event_slug] += op.count

        writer = csv.writer(stdout, dialect="excel")
        writer.writerow(["days_to_event", *event_slugs])

        cumulative = Counter()

        for days_to_event in range(min(stats.keys()), max(stats.keys()) + 1):
            row = [days_to_event]

            for event_slug in event_slugs:
                cumulative[event_slug] += stats[days_to_event][event_slug]
                row.append(cumulative[event_slug])

            writer.writerow(row)
