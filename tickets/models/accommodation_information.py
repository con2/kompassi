import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.csv_export import CsvExportMixin
from core.utils import phone_number_validator

from .limit_group import LimitGroup
from .order_product import OrderProduct

logger = logging.getLogger("kompassi")


class AccommodationInformation(models.Model, CsvExportMixin):
    order_product = models.ForeignKey(
        OrderProduct,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="accommodation_information_set",
    )

    # XXX ugly hack: We hijack limit groups to represent (night, accommodation centre).
    limit_groups = models.ManyToManyField(LimitGroup, blank=True, related_name="accommodation_information_set")

    # allow blank because these are pre-created
    first_name = models.CharField(max_length=100, blank=True, default="", verbose_name="Etunimi")
    last_name = models.CharField(max_length=100, blank=True, default="", verbose_name="Sukunimi")

    phone_number = models.CharField(
        max_length=30,
        blank=True,
        default="",
        validators=[phone_number_validator],
        verbose_name="Puhelinnumero",
    )

    email = models.EmailField(blank=True, default="", verbose_name="Sähköpostiosoite")

    class State(models.TextChoices):
        NOT_ARRIVED = "N", _("Not arrived")
        ARRIVED = "A", _("Arrived")
        LEFT = "L", _("Left")

    state = models.CharField(
        max_length=1,
        default=State.NOT_ARRIVED,
        verbose_name=_("State"),
        choices=State.choices,
    )
    room_name = models.CharField(
        max_length=63,
        blank=True,
        default="",
        verbose_name="Majoitustila",
    )

    @classmethod
    def get_for_order(cls, order):
        ais = []

        for order_product in order.order_product_set.filter(
            count__gt=0, product__requires_accommodation_information=True
        ):
            op_ais = list(order_product.accommodation_information_set.all())

            while len(op_ais) > order_product.count:
                op_ais[-1].delete()
                op_ais.pop()

            while len(op_ais) < order_product.count:
                op_ais.append(cls.objects.create(order_product=order_product))

            ais.extend(op_ais)

        return ais

    @property
    def event(self):
        # cannot use order_product because it can be None
        first_limit_group = self.limit_groups.first()
        return first_limit_group.event if first_limit_group else None

    @property
    def product_name(self):
        first_limit_group = self.limit_groups.first()
        return first_limit_group.description if first_limit_group else None

    @property
    def formatted_order_number(self):
        return self.order_product.order.formatted_order_number if self.order_product else ""

    @property
    def is_present(self):
        return self.state == AccommodationInformation.State.ARRIVED

    @property
    def row_css_class(self):
        return "success" if self.is_present else ""

    def get_presence_form(self):
        from ..forms import AccommodationPresenceForm

        return AccommodationPresenceForm(instance=self)

    @classmethod
    def get_csv_fields(cls, event):
        return (
            (cls, "formatted_order_number"),
            (cls, "last_name"),
            (cls, "first_name"),
            (cls, "phone_number"),
            (cls, "email"),
        )

    def get_csv_related(self):
        return {}

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "majoittujan tiedot"
        verbose_name_plural = "majoittujan tiedot"
