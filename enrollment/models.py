# encoding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import EventMetaBase
from core.utils import alias_property


"""
Holds all the possible fields an enrollment instance may have
"""
class Enrollment(models.Model):
    event = models.ForeignKey('core.event')
    person = models.ForeignKey('core.person')


"""
An event creates an instance of this class to indicate use of enrollment module
"""
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


