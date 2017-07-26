#!/usr/bin/env python
# encoding: utf-8
# vim: shiftwidth=4 expandtab

import csv
import sys

from django.core.management.base import BaseCommand
from tickets.models import *


def u(unicode_str):
    return unicode_str.encode('UTF-8')


class Command(BaseCommand):
    args = '<id>'
    help = 'Print orders that include the given product'

    def handle(*args, **options):
        product_id = int(args[1])
        writer = csv.writer(sys.stdout)
        writer.writerow(['last_name', 'first_name', 'email', 'count'])

        product = Product.objects.get(id=product_id)
        for op in product.order_product_set.filter(
            count__gt=0,
            order__confirm_time__isnull=False,
            order__payment_date__isnull=False,
            order__cancellation_time__isnull=True,
        ).order_by('order__customer__last_name', 'order__customer__first_name'):
            customer = op.order.customer
            writer.writerow([
                u(customer.last_name),
                u(customer.first_name),
                u(customer.email),
                op.count,
            ])
