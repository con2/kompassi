# encoding: utf-8



import logging

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from dateutil.parser import parse as parse_datetime
from six import text_type
import openpyxl

from core.models import Event
from tickets.models import Customer, Order, Product, OrderProduct


logger = logging.getLogger('kompassi')


class Command(BaseCommand):
    help = 'Creates orders and sends e-tickets based on an XLSX export from Holvi'

    def add_arguments(self, parser):
        parser.add_argument('event_slug', type=text_type)
        parser.add_argument('product_id', type=int)
        parser.add_argument('xlsx_file', type=text_type)

    def handle(self, *args, **options):
        event = Event.objects.get(slug=options['event_slug'])
        product = Product.objects.get(id=options['product_id'], event=event)

        workbook = openpyxl.load_workbook(filename=options['xlsx_file'], read_only=True)
        worksheet = workbook.active

        rows_iter = worksheet.rows
        header_row = next(rows_iter)

        for row in rows_iter:
            row_dict = dict(list(zip(
                (c.value for c in header_row),
                (c.value for c in row)
            )))

            email = row_dict['Sähköpostiosoite, johon toimitamme PDF-lipun']
            if not email:
                email = row_dict['Sähköposti']
            if not email:
                logger.warn('No e-mail address in row %s', row_dict)
                continue

            payment_date = parse_datetime(row_dict['Päiväys']).date()
            first_name = row_dict['Etunimi']
            last_name = row_dict['Sukunimi']

            with transaction.atomic():
                customer = Customer(
                    first_name=first_name,
                    last_name=last_name,
                    address='',
                    zip_code='',
                    city='',
                    email=email,
                    allow_marketing_email=False,
                )
                customer.save()

                order = Order(event=event, customer=customer)
                order.save()

                order_product = OrderProduct(
                    order=order,
                    product=product,
                    count=1,
                )
                order_product.save()

            order.confirm_order()
            order.confirm_payment(
                payment_date=payment_date,
                send_email=True,
            )

            print(first_name, last_name)
