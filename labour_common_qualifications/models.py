# encoding: utf-8

from django.db import models
from django.core.validators import RegexValidator

from labour.models import QualificationExtraBase

validate_jv_card_number = RegexValidator(
    regex=r'\d\d\d\d/J\d\d\d\d/\d\d',
    message=u"Tarkista JV-kortin numero"
)

class JVKortti(QualificationExtraBase):
    card_number = models.CharField(
        max_length='13',
        validators=[validate_jv_card_number,],
        verbose_name=u"JV-kortin numero"
    )

    expiration_date = models.DateField(verbose_name=u"Viimeinen voimassaolopäivä")

    @classmethod
    def init_form(cls, *args, **kwargs):
        from .forms import JVKorttiForm
        return JVKorttiForm(*args, **kwargs)

    class Meta:
        verbose_name = u"JV-kortti"
        verbose_name_plural = u"JV-kortit"