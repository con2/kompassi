# encoding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from core.utils import SLUG_FIELD_PARAMS, NONUNIQUE_SLUG_FIELD_PARAMS


@python_2_unicode_compatible
class Survey(models.Model):
    # Subclasses must provide a `slug` field
    # slug = models.CharField(...)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    model = JSONField(help_text=_(
        'Use the <a href="http://surveyjs.org/builder/">Survey.JS Builder</a> to create the survey.'
    ))

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class EventSurvey(Survey):
    event = models.ForeignKey('core.Event')
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)

    def get_absolute_url(self):
        return reverse('event_survey_view', kwargs=dict(event_slug=self.event.slug, survey_slug=self.slug))

    class Meta:
        unique_together = [('event', 'slug')]


class GlobalSurvey(Survey):
    slug = models.CharField(**SLUG_FIELD_PARAMS)

    def get_absolute_url(self):
        return reverse('global_survey_view', kwargs=dict(survey_slug=self.slug))
