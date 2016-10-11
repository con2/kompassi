# encoding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import EventMetaBase
from core.utils import alias_property


class SimpleChoice(models.Model):
    """
    Abstract base model for generic simple M2M fields.
    """

    name = models.CharField(max_length=63)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class SpecialDiet(SimpleChoice):
    pass


class Enrollment(models.Model):
    """
    Holds all the possible fields an enrollment instance may have
    """
    event = models.ForeignKey('core.event')
    person = models.ForeignKey('core.person')

    special_diet = models.ManyToManyField(
        SpecialDiet,
        blank=True,
        verbose_name=_("Diet")
    )

    special_diet_other = models.TextField(
        blank=True,
        verbose_name=_('Other diets'),
        help_text=_(
            'If you\'re on a diet that\'s not included in the list, '
            'please detail your diet here. Event organizer will try '
            'to take dietary needs into consideration, but all diets '
            'may not be catered for.'
        )
    )



"""
An event creates an instance of this class to indicate use of enrollment module
"""
class EnrollmentEventMeta(EventMetaBase):
    form_code_path = models.CharField(
        max_length=63,
        help_text=_("Reference to form class. Example: events.yukicon2016.forms:EnrollmentForm"),
    );

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

    @property
    def form_code(self):
        if not getattr(self, '_form_code', None):
            from core.utils import get_code
            self._form_code = get_code(self.form_code_path)

        return self._form_code

