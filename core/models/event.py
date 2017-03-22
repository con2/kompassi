# encoding: utf-8

import logging
from datetime import timedelta

from django.conf import settings
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

    name = models.CharField(max_length=63, verbose_name='Tapahtuman nimi')

    organization = models.ForeignKey('core.Organization', verbose_name='Järjestäjätaho')

    name_genitive = models.CharField(
        max_length=63,
        verbose_name='Tapahtuman nimi genetiivissä',
        help_text='Esimerkki: Susiconin',
    )

    name_illative = models.CharField(
        max_length=63,
        verbose_name='Tapahtuman nimi illatiivissä',
        help_text='Esimerkki: Susiconiin',
    )

    name_inessive = models.CharField(
        max_length=63,
        verbose_name='Tapahtuman nimi inessiivissä',
        help_text='Esimerkki: Susiconissa',
    )

    description = models.TextField(blank=True, verbose_name='Kuvaus')

    venue = models.ForeignKey('core.Venue',
        verbose_name='Tapahtumapaikka',
    )

    start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Alkamisaika',
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Päättymisaika',
    )

    homepage_url = models.CharField(
        blank=True,
        max_length=255,
        verbose_name='Tapahtuman kotisivu',
    )

    public = models.BooleanField(
        default=True,
        verbose_name='Julkinen',
        help_text='Julkiset tapahtumat näytetään etusivulla.'
    )

    logo_url = models.CharField(
        blank=True,
        max_length=255,
        default='',
        verbose_name='Tapahtuman logon URL',
        help_text='Voi olla paikallinen (alkaa /-merkillä) tai absoluuttinen (alkaa http/https)',
    )

    description = models.TextField(
        blank=True,
        default='',
        verbose_name='Tapahtuman kuvaus',
        help_text='Muutaman kappaleen mittainen kuvaus tapahtumasta. Näkyy tapahtumasivulla.',
    )

    class Meta:
        verbose_name = 'Tapahtuma'
        verbose_name_plural = 'Tapahtumat'

    def __init__(self, *args, **kwargs):
        # Avoid having to manually transform 20 or so event setup scripts with organization_name and organization_url
        # in get_or_create.defaults
        if 'organization_name' in kwargs:
            from .organization import Organization

            organization_name = kwargs.pop('organization_name')
            organization_url = kwargs.pop('organization_url', '')

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
        return "{name} ({year})".format(
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

        return ' '.join(headline_parts)

    @classmethod
    def get_or_create_dummy(cls):
        from .venue import Venue
        from .organization import Organization

        # TODO not the best place for this, encap. see also admin command core_update_maysendinfo
        from django.contrib.auth.models import Group
        Group.objects.get_or_create(name=settings.KOMPASSI_MAY_SEND_INFO_GROUP_NAME)

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

    labour_event_meta = event_meta_property('labour')
    programme_event_meta = event_meta_property('programme')
    badges_event_meta = event_meta_property('badges')
    tickets_event_meta = event_meta_property('tickets')
    payments_event_meta = event_meta_property('payments')
    sms_event_meta = event_meta_property('sms')
    enrollment_event_meta = event_meta_property('enrollment')
    intra_event_meta = event_meta_property('intra')

    def app_event_meta(self, app_label):
        return getattr(self, '{}_event_meta'.format(app_label))

    def as_dict(self):
        return pick_attrs(self,
            'slug',
            'name',
            'homepage_url',
            'headline',

            organization=self.organization.as_dict(),
        )
