from itertools import chain

from django.db import models
from django.utils.timezone import now

from core.utils import SLUG_FIELD_PARAMS, format_date_range, pick_attrs


class Listing(models.Model):
    hostname = models.CharField(
        max_length=63,
        unique=True,
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')

    events = models.ManyToManyField('core.Event')
    external_events = models.ManyToManyField('listings.ExternalEvent')

    def get_events(self, **criteria):
        from core.models import Event

        external_events = self.external_events.filter(**criteria).order_by('start_time')
        events = self.events.filter(start_time__isnull=False, **criteria).order_by('start_time')

        return sorted(chain(external_events, events), key=lambda e: e.start_time)

    def __str__(self):
        return self.title

    def as_dict(self):
        t = now()

        return pick_attrs(self,
            'hostname',
            'title',

            events=[event.as_dict(format='listing') for event in self.get_events(public=True, end_time__gt=t)],
        )


class ExternalEvent(models.Model):
    '''
    Minimal details about an external event. API is a subset of Event.
    '''

    slug = models.CharField(**SLUG_FIELD_PARAMS)
    name = models.CharField(max_length=63, verbose_name='Tapahtuman nimi')
    description = models.TextField(blank=True, verbose_name='Kuvaus')
    homepage_url = models.CharField(
        blank=True,
        max_length=255,
        verbose_name='Tapahtuman kotisivu',
    )
    venue_name = models.CharField(max_length=63, blank=True)

    # should be named is_public but due to legacy
    public = models.BooleanField(default=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.name

    @property
    def formatted_start_and_end_date(self):
        return format_date_range(self.start_time, self.end_time)

    @property
    def headline(self):
        headline_parts = [
            self.venue_name,
            (self.formatted_start_and_end_date if self.start_time and self.end_time else None),
        ]
        headline_parts = [part for part in headline_parts if part]

        return ' '.join(headline_parts)

    def as_dict(self, format='listing'):
        assert format == 'listing'

        return pick_attrs(self,
            'slug',
            'name',
            'headline',
            'venue_name',
            'homepage_url',
            'start_time',
            'end_time',
        )
