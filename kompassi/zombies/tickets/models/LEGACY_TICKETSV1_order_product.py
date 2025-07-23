import logging

from django.db import models

from kompassi.core.csv_export import CsvExportMixin
from kompassi.core.utils.cleanup import register_cleanup

from ..utils import format_price
from .LEGACY_TICKETSV1_order import Order
from .LEGACY_TICKETSV1_product import Product

logger = logging.getLogger(__name__)


@register_cleanup(lambda qs: qs.filter(count=0))
class OrderProduct(models.Model, CsvExportMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_product_set")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_product_set")
    count = models.IntegerField(default=0)

    @property
    def target(self):
        return self.product

    @property
    def price_cents(self):
        return self.count * self.product.price_cents

    @property
    def formatted_price(self):
        return format_price(self.price_cents)

    @property
    def description(self):
        product_name = self.product.name if self.product is not None else None
        return f"{self.count}x {product_name}"

    @classmethod
    def get_csv_fields(cls, event):
        return [
            (Order, "payment_date"),
            (Order, "formatted_order_number"),
            (Product, "name"),
            (Product, "price_cents"),
            (cls, "count"),
            (cls, "price_cents"),
        ]

    @classmethod
    def get_csv_header(cls, event, fields, m2m_mode):
        return [
            "payment_date",
            "order_number",
            "product_name",
            "product_price_cents",
            "count",
            "row_price_cents",
        ]

    def get_csv_related(self):
        return {
            Order: self.order,
            Product: self.product,
        }

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "tilausrivi"
        verbose_name_plural = "tilausrivit"
        unique_together = [("order", "product")]
