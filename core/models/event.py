# encoding: utf-8

import logging
from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from ..utils import (
    format_date_range,
    pick_attrs,
    SLUG_FIELD_PARAMS,
    slugify,
    event_meta_property,
)


logger = logging.getLogger('kompassi')


class Event(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)

    name = models.CharField(max_length=63, verbose_name=u'Tapahtuman nimi')

    organization = models.ForeignKey('core.Organization', verbose_name=u'Järjestäjätaho')

    name_genitive = models.CharField(
        max_length=63,
        verbose_name=u'Tapahtuman nimi genetiivissä',
        help_text=u'Esimerkki: Susiconin',
    )

    name_illative = models.CharField(
        max_length=63,
        verbose_name=u'Tapahtuman nimi illatiivissä',
        help_text=u'Esimerkki: Susiconiin',
    )

    name_inessive = models.CharField(
        max_length=63,
        verbose_name=u'Tapahtuman nimi inessiivissä',
        help_text=u'Esimerkki: Susiconissa',
    )

    description = models.TextField(blank=True, verbose_name=u'Kuvaus')

    venue = models.ForeignKey('core.Venue',
        verbose_name=u'Tapahtumapaikka',
    )

    start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Alkamisaika',
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Päättymisaika',
    )

    homepage_url = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=u'Tapahtuman kotisivu',
    )

    public = models.BooleanField(
        default=True,
        verbose_name=u'Julkinen',
        help_text=u'Julkiset tapahtumat näytetään etusivulla.'
    )

    logo_url = models.CharField(
        blank=True,
        max_length=255,
        default='',
        verbose_name=u'Tapahtuman logon URL',
        help_text=u'Voi olla paikallinen (alkaa /-merkillä) tai absoluuttinen (alkaa http/https)',
    )

    description = models.TextField(
        blank=True,
        default='',
        verbose_name=u'Tapahtuman kuvaus',
        help_text=u'Muutaman kappaleen mittainen kuvaus tapahtumasta. Näkyy tapahtumasivulla.',
    )

    class Meta:
        verbose_name = u'Tapahtuma'
        verbose_name_plural = u'Tapahtumat'

    def __init__(self, *args, **kwargs):
        # Avoid having to manually transform 20 or so event setup scripts with organization_name and organization_url
        # in get_or_create.defaults
        if 'organization_name' in kwargs:
            from .organization import Organization

            organization_name = kwargs.pop('organization_name')
            organization_url = kwargs.pop('organization_url', u'')

            kwargs['organization'], unused = Organization.objects.get_or_create(
                slug=slugify(organization_name),
                defaults=dict(
                    name=organization_name,
                    homepage_url=organization_url,
                )
            )

        super(Event, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            for field, suffix in [
                ('name_genitive', 'in'),
                ('name_illative', 'iin'),
                ('name_inessive', 'issa'),
            ]:
                if not getattr(self, field, None):
                    setattr(self, field, self.name + suffix)

        return super(Event, self).save(*args, **kwargs)

    @property
    def name_and_year(self):
        return u"{name} ({year})".format(
            name=self.name,
            year=self.start_time.year,
        )

    @property
    def formatted_start_and_end_date(self):
        return format_date_range(self.start_time, self.end_time)

    @property
    def headline(self):
        headline_parts = [
            (self.venue.name_inessive if self.venue else None),
            (self.formatted_start_and_end_date if self.start_time and self.end_time else None),
        ]
        headline_parts = [part for part in headline_parts if part]

        return u' '.join(headline_parts)

    @classmethod
    def get_or_create_dummy(cls):
        from .venue import Venue
        from .organization import Organization

        venue, unused = Venue.get_or_create_dummy()
        organization, unused = Organization.get_or_create_dummy()
        t = timezone.now()

        return cls.objects.get_or_create(
            name='Dummy event',
            defaults=dict(
                venue=venue,
                start_time=t + timedelta(days=60),
                end_time=t + timedelta(days=61),
                slug='dummy',
                organization=organization,
            ),
        )

    labour_event_meta = event_meta_property('labour', 'labour.models:LabourEventMeta')
    programme_event_meta = event_meta_property('programme', 'programme.models:ProgrammeEventMeta')
    badges_event_meta = event_meta_property('badges', 'badges.models:BadgesEventMeta')
    tickets_event_meta = event_meta_property('tickets', 'tickets.models:TicketsEventMeta')
    payments_event_meta = event_meta_property('payments', 'payments.models:PaymentsEventMeta')
    sms_event_meta = event_meta_property('sms', 'sms.models:SMSEventMeta')
    enrollment_event_meta = event_meta_property('enrollment', 'enrollment.models:EnrollmentEventMeta')

    def app_event_meta(self, app_label):
        return getattr(self, '{}_event_meta'.format(app_label))

    def as_dict(self):
        return pick_attrs(self,
            'slug',
            'name',
        )
