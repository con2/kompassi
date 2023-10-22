from django.test import TestCase

from .models import LimitGroup, Product, Order


class LimitGroupsTestCase(TestCase):
    def test_amount_available(self):
        limit_saturday, limit_sunday = LimitGroup.get_or_create_dummies()
        weekend, saturday, sunday = Product.get_or_create_dummies()

        assert limit_saturday in weekend.limit_groups.all()
        assert limit_sunday in weekend.limit_groups.all()
        assert limit_saturday in saturday.limit_groups.all()
        assert limit_sunday in sunday.limit_groups.all()

        assert weekend.in_stock
        assert saturday.in_stock
        assert sunday.in_stock

        order, unused = Order.get_or_create_dummy()
        order.confirm_order()

        order.order_product_set.create(product=saturday, count=2000)
        order.order_product_set.create(product=sunday, count=1500)
        order.order_product_set.create(product=weekend, count=3000)

        # saturday + weekend now 5000 which is the limit
        # sunday + weekend now 4500 which is below the limit

        weekend.refresh_from_db()
        saturday.refresh_from_db()
        sunday.refresh_from_db()

        assert not weekend.in_stock
        assert not saturday.in_stock
        assert sunday.in_stock
