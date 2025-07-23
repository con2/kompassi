import logging
from functools import cached_property
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from .LEGACY_TICKETSV1_consts import LOW_AVAILABILITY_THRESHOLD

if TYPE_CHECKING:
    from .LEGACY_TICKETSV1_product import Product


logger = logging.getLogger(__name__)


class LimitGroup(models.Model):
    id: int
    pk: int
    product_set: models.QuerySet["Product"]

    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, verbose_name=_("Event"))
    description = models.CharField(max_length=255, verbose_name=_("Description"))
    limit = models.IntegerField(verbose_name=_("Maximum amount to sell"))

    def __str__(self):
        return f"{self.description} ({self.amount_available}/{self.limit})"

    class Meta:
        verbose_name = _("limit group")
        verbose_name_plural = _("limit groups")

    @cached_property
    def amount_sold(self):
        from .LEGACY_TICKETSV1_order_product import OrderProduct

        amount_sold = OrderProduct.objects.filter(
            product__limit_groups=self,
            order__confirm_time__isnull=False,
            order__cancellation_time__isnull=True,
        ).aggregate(models.Sum("count"))["count__sum"]

        return amount_sold if amount_sold is not None else 0

    def refresh_from_db(self, *args, **kwargs):
        super().refresh_from_db(*args, **kwargs)

        # invalidate cached properties
        self.__dict__.pop("amount_sold", None)

    @property
    def amount_available(self):
        return self.limit - self.amount_sold

    @property
    def is_sold_out(self):
        return self.amount_available < 1

    @property
    def is_availability_low(self):
        return self.amount_available < LOW_AVAILABILITY_THRESHOLD

    @property
    def css_class(self):
        if self.is_sold_out:
            return "danger"
        elif self.is_availability_low:
            return "warning"
        else:
            return ""

    @classmethod
    def get_or_create_dummies(cls):
        from kompassi.core.models import Event

        event, unused = Event.get_or_create_dummy()

        limit_saturday, unused = cls.objects.get_or_create(
            event=event, description="Testing saturday", defaults=dict(limit=5000)
        )
        limit_sunday, unused = cls.objects.get_or_create(
            event=event, description="Testing sunday", defaults=dict(limit=5000)
        )

        return [limit_saturday, limit_sunday]
