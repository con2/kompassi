# encoding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, code_property, is_within_period


@python_2_unicode_compatible
class Survey(models.Model):
    """
    The Labour Manager may have their Workers fill in a Survey some time after signing up.
    The driving use case for these Surveys is to ask for shift wishes some time before the event.
    A Survey requires a Model and a Form. The Model is requested to return an instance via
    Model.for_signup(signup) and it is passed to the Form via
    initialize_form(Form, request, instance=instance, event=event).
    """

    event = models.ForeignKey('core.Event')
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)
    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'),
        help_text=_('Will be displayed at the top of the survey page.'),
    )
    description = models.TextField(
        verbose_name=_('Description'),
        help_text=_('Will be displayed at the top of the survey page.'),
    )

    active_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Active from'),
    )

    active_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Active until'),
    )

    form_class_path = models.CharField(
        max_length=255,
        verbose_name=_('Form path'),
        help_text=_('A reference to the form that is used as the survey form.'),
    )

    form_class = code_property('form_class_path')

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        return is_within_period(self.active_from, self.active_until)

    def admin_is_active(self):
        return self.is_active
    admin_is_active.short_description = _('Active')
    admin_is_active.boolean = True

    class Meta:
        verbose_name = _('Survey')
        verbose_name_plural = _('Surveys')
        unique_together = [
            ('event', 'slug'),
        ]
