import logging
from functools import cached_property
from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.core.models import Event

from ..utils import format_price
from .LEGACY_TICKETSV1_consts import LOW_AVAILABILITY_THRESHOLD

logger = logging.getLogger(__name__)


class Product(models.Model):
    id: int
    pk: int

    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    name = models.CharField(max_length=150)
    override_electronic_ticket_title = models.CharField(max_length=100, default="", blank=True)

    internal_description = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField()
    mail_description = models.TextField(null=True, blank=True)
    limit_groups = models.ManyToManyField("tickets.LimitGroup", blank=True)
    price_cents = models.IntegerField()
    electronic_ticket = models.BooleanField(default=False)
    electronic_tickets_per_product = models.PositiveIntegerField(default=1)
    available = models.BooleanField(default=True)
    notify_email = models.CharField(max_length=100, null=True, blank=True)
    ordering = models.IntegerField(default=0)
    code = models.CharField(
        max_length=63,
        blank=True,
        default="",
        help_text="If set, the product will only be available with this code supplied as a query string parameter.",
    )

    @property
    def electronic_ticket_title(self):
        if self.override_electronic_ticket_title:
            return self.override_electronic_ticket_title
        else:
            return self.name

    @property
    def sell_limit(self):
        from warnings import warn

        warn(
            "sell_limit is deprecated, convert everything to use LimitGroup and amount_available directly",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.amount_available

    @property
    def formatted_price(self):
        return format_price(self.price_cents)

    @property
    def in_stock(self):
        return self.amount_available > 0

    @property
    def availability_low(self):
        return self.amount_available < LOW_AVAILABILITY_THRESHOLD

    @cached_property
    def amount_available(self):
        return min(group.amount_available for group in self.limit_groups.all())

    def refresh_from_db(self, *args, **kwargs):
        super().refresh_from_db(*args, **kwargs)

        # invalidate cached properties
        self.__dict__.pop("amount_available", None)

    @property
    def amount_sold(self):
        from .LEGACY_TICKETSV1_order_product import OrderProduct

        cnt = OrderProduct.objects.filter(
            product=self, order__confirm_time__isnull=False, order__cancellation_time__isnull=True
        ).aggregate(models.Sum("count"))

        sm = cnt["count__sum"]
        return sm if sm is not None else 0

    def __str__(self):
        return f"{self.name} ({self.formatted_price})"

    class Meta:
        ordering = ("ordering", "id")
        verbose_name = _("product")
        verbose_name_plural = _("products")

    @classmethod
    def get_or_create_dummy(cls, name="Dummy product", limit_groups=None):
        from .LEGACY_TICKETSV1_tickets_event_meta import TicketsEventMeta

        if limit_groups is None:
            limit_groups = []
        meta, unused = TicketsEventMeta.get_or_create_dummy()

        dummy, created = cls.objects.get_or_create(
            event=meta.event,
            name=name,
            defaults=dict(
                description="Dummy product for testing",
                price_cents=1800,
                available=True,
                ordering=100,
                electronic_ticket=True,
            ),
        )

        if created:
            dummy.limit_groups.set(limit_groups)

        return dummy, created

    @classmethod
    def get_or_create_dummies(cls):
        from .LEGACY_TICKETSV1_limit_group import LimitGroup

        [limit_saturday, limit_sunday] = LimitGroup.get_or_create_dummies()

        weekend, unused = cls.get_or_create_dummy("Weekend test product", [limit_saturday, limit_sunday])
        saturday, unused = cls.get_or_create_dummy("Saturday test product", [limit_saturday])
        sunday, unused = cls.get_or_create_dummy("Sunday test product", [limit_sunday])

        return [weekend, saturday, sunday]

    @classmethod
    def get_products_for_event(cls, event: "Event", code: str = "", admin: bool = False):
        """
        Returns a list of products that are available for the given event and code.
        """
        criteria: dict[str, Any] = dict(event=event)
        if not admin:
            criteria.update(code=code, available=True)
        return cls.objects.filter(**criteria).order_by("ordering", "id")
