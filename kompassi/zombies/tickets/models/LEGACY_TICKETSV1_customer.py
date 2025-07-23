import logging

import phonenumbers
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import (
    format_phone_number,
    phone_number_validator,
)
from kompassi.core.utils.cleanup import register_cleanup

logger = logging.getLogger(__name__)


@register_cleanup(lambda qs: qs.filter(order__isnull=True))
class Customer(models.Model):
    # REVERSE: order = OneToOne(Order)

    first_name = models.CharField(max_length=100, verbose_name=_("First name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Surname"))

    email = models.EmailField(
        verbose_name=_("E-mail address"),
        help_text=_(
            "Check the e-mail address carefully. The order confirmation and any electronic tickets "
            "will be sent to this e-mail address."
        ),
    )

    phone_number = models.CharField(
        max_length=30,
        blank=True,
        validators=[phone_number_validator],
        verbose_name=_("phone number"),
        default="",
    )

    def get_normalized_phone_number(
        self,
        region=settings.KOMPASSI_PHONENUMBERS_DEFAULT_REGION,
        format=settings.KOMPASSI_PHONENUMBERS_DEFAULT_FORMAT,
    ):
        """
        Returns the phone number of this Customer in a normalized format. If the phone number is invalid,
        this is logged, and the invalid phone number is returned as-is.
        """

        if not self.phone_number:
            return ""

        try:
            return format_phone_number(self.phone_number, region=region, format=format)
        except phonenumbers.NumberParseException:
            return self.phone_number

    @property
    def normalized_phone_number(self):
        return self.get_normalized_phone_number()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("customer")
        verbose_name_plural = _("customers")

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def sanitized_name(self):
        return "".join(i for i in self.name if i.isalpha() or i in ("ä", "Ä", "ö", "Ö", "å", "Å", "-", "'", " "))

    @property
    def name_and_email(self):
        return f"{self.sanitized_name} <{self.email}>"

    @classmethod
    def get_or_create_dummy(cls):
        return cls.objects.get_or_create(
            first_name="Dummy",
            last_name="Testinen",
            defaults=dict(
                email="dummy@example.com",
                phone_number="+358 50 0000",
            ),
        )
