import logging

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from core.utils import SLUG_FIELD_PARAMS, NONUNIQUE_SLUG_FIELD_PARAMS, slugify


logger = logging.getLogger('kompassi')


class Survey(models.Model):
    # Subclasses must provide a `slug` field
    # slug = models.CharField(...)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    model = JSONField(help_text=_(
        'Use the <a href="http://surveyjs.org/builder/" target="_blank">Survey.JS Builder</a> '
        'to create the survey.'
    ))

    def __str__(self):
        return self.title

    @property
    def field_names(self):
        if not self.model:
            return []

        def _generator():
            for page in self.model['pages']:
                for element in page['elements']:
                    yield element['name']

        return list(_generator())

    class Meta:
        abstract = True


class EventSurvey(Survey):
    event = models.ForeignKey('core.Event', on_delete=models.CASCADE)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)

    def get_absolute_url(self):
        return reverse('event_survey_view', kwargs=dict(event_slug=self.event.slug, survey_slug=self.slug))

    @classmethod
    def get_or_create_dummy(cls, event=None, title="Dummy survey", **kwargs):
        if event is None:
            from core.models import Event
            event, unused = Event.get_or_create_dummy()

        slug = slugify(title)

        defaults = dict(
            event=event,
            title=title,
            model=dict(),
        )
        defaults.update(kwargs)

        return cls.objects.get_or_create(
            slug=slug,
            defaults=defaults,
        )

    class Meta:
        unique_together = [('event', 'slug')]


class GlobalSurvey(Survey):
    slug = models.CharField(**SLUG_FIELD_PARAMS)

    def get_absolute_url(self):
        return reverse('global_survey_view', kwargs=dict(survey_slug=self.slug))
