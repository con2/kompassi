# encoding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import EventMetaBase
from core.utils import alias_property

# Sisältää kaikki kentät, joita ilmoittautumisessa on mahdollista käyttää
class Enrollment(models.Model):
    event = models.ForeignKey('core.event')
#    person = models.ForeignKey('core.person')
    # lisää kenttiä tähän

# Tapahtuma käyttää tätä kertomaan, käyttääkö enrollment-moduulia
# Todo mitkä ovat lopulliset kentät?
class EnrollmentEventMeta(EventMetaBase):
    enrollment_opens = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Enrollment opens"),
    )
    public_from = alias_property('enrollment_opens')

    enrollment_closes = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Enrollment closes"),
    )
    public_until = alias_property('enrollment_closes')


