from django.test import TestCase

from tickets.models import Order
from payments.models import PaymentsEventMeta


class FakeRequest(object):
    def build_absolute_uri(self, uri):
        return 'https://localhost:8000' + uri

class CheckoutTestCase(TestCase):
    def test_checkout(self):
        request = FakeRequest()

        PaymentsEventMeta.get_or_create_dummy()

        order, unused = Order.get_or_create_dummy()

        # TODO write better tests
        # now we just check it doesn't throw
        order.checkout_mac(request)
        order.checkout_return_url(request)
