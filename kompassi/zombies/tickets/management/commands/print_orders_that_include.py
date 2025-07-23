#!/usr/bin/env python
# vim: shiftwidth=4 expandtab

import csv
import sys

from django.core.management.base import BaseCommand

from kompassi.zombies.tickets.models import Product


class Command(BaseCommand):
    args = "<id>"
    help = "Print orders that include the given product"

    def add_arguments(self, parser):
        parser.add_argument("product", type=int, help="product id")

    def handle(*args, **options):
        product_id = int(options["product"])
        writer = csv.writer(sys.stdout)
        writer.writerow(["last_name", "first_name", "email", "count"])

        product = Product.objects.get(id=product_id)
        for op in product.order_product_set.filter(
            count__gt=0,
            order__confirm_time__isnull=False,
            order__payment_date__isnull=False,
            order__cancellation_time__isnull=True,
        ).order_by("order__customer__last_name", "order__customer__first_name"):
            customer = op.order.customer
            writer.writerow(
                [
                    customer.last_name,
                    customer.first_name,
                    customer.email,
                    op.count,
                ]
            )
