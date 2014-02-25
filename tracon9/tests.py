# encoding: utf-8

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from core.models import Event
from tickets.models import Product, Order, OrderProduct
from lippukala.models import Code, Order as LippukalaOrder
from tracon9.lippukala_integration import Queue

class Tracon9LippukalaTestCase(TestCase):
    def test_manual_code_creation(self):
        if 'lippukala' not in settings.INSTALLED_APPS:
            print 'Test disabled due to lippukala not being installed'
            return

        call_command('setup_core', test=True)
        call_command('setup_labour_common_qualifications', test=True)
        call_command('setup_tracon9', test=True)

        num_tickets = 2

        event = Event.objects.get(name='Tracon 9')
        product = Product.objects.get(event=event, name__icontains='viikonlop', electronic_ticket=True)
        order, created = Order.get_or_create_dummy(event=event)
        OrderProduct.objects.get_or_create(order=order, product=product, count=num_tickets)

        lippukala_order = LippukalaOrder.objects.create(
            address_text=order.formatted_address,
            free_text=u"Tervetuloa Traconiin!",
            comment=u"Mihis tää tulee?",
            reference_number=order.reference_number,
        )

        codes = [Code.objects.create(
            order=lippukala_order,
            prefix=order.lippukala_prefix,
            product_text=product.name,
        ) for i in xrange(num_tickets)]

        for code in codes:
            print code.full_code, code.literate_code
            assert code.full_code.startswith(Queue.TWO_WEEKEND_TICKETS)
            assert code.literate_code.startswith(settings.LIPPUKALA_PREFIXES[Queue.TWO_WEEKEND_TICKETS])
