from django.db import models

from tickets.models import Order, Customer, ShirtOrder


class CustomShirtsManager(models.Manager):
    def get_queryset(self):
        customization_orders = Order.objects.filter(
            event__slug='traconpaidat2019',
            order_product_set__count__gt=0,
            order_product_set__product__name='Nimikointi',
            confirm_time__isnull=False,
            payment_date__isnull=False,
            cancellation_time__isnull=True,
        )

        return super().get_queryset().filter(order__in=customization_orders)


class CustomShirtProxy(ShirtOrder):
    objects = CustomShirtsManager()

    @classmethod
    def get_csv_fields(cls, event):
        return (
            (Customer, 'first_name'),
            (cls, 'csv_type'),
            (cls, 'csv_size'),
            (cls, 'count'),
        )

    def get_csv_related(self):
        return {
            Customer: self.order.customer,
        }

    class Meta:
        proxy = True
