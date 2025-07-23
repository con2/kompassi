from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.dateformat import format as format_date

from kompassi.labour.models import QualificationExtraBase

validate_jv_card_number = RegexValidator(regex=r".+/.+/.+", message="Tarkista JV-kortin numero")


class JVKortti(QualificationExtraBase):
    card_number = models.CharField(
        max_length=13,
        validators=[
            validate_jv_card_number,
        ],
        verbose_name="JV-kortin numero",
        help_text="Muoto: 0000/J0000/00 tai XX/0000/00",
    )

    expiration_date = models.DateField(verbose_name="Viimeinen voimassaolopäivä")

    def __str__(self):
        n = self.card_number
        d = format_date(self.expiration_date, settings.DATE_FORMAT)

        return f"{n}, voimassa {d} asti"

    @classmethod
    def get_form_class(cls):
        from .forms import JVKorttiForm

        return JVKorttiForm

    class Meta:
        verbose_name = "JV-kortti"
        verbose_name_plural = "JV-kortit"
