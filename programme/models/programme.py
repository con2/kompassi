# encoding: utf-8

import logging
import datetime
from datetime import timedelta

from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.contrib import messages
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from dateutil.tz import tzlocal

from core.csv_export import CsvExportMixin
from core.models import EventMetaBase, OneTimeCode
from core.utils import (
    alias_property,
    format_datetime,
    full_hours_between,
    get_previous_and_next,
    NONUNIQUE_SLUG_FIELD_PARAMS,
    slugify,
    url,
)

from ..utils import window, next_full_hour


RECORDING_PERMISSION_CHOICES = [
    (u'public', u'Ohjelmanumeroni saa videoida ja julkaista'),
    (u'private', u'Kiellän ohjelmanumeroni julkaisun, mutta sen saa videoida arkistokäyttöön'),
    (u'forbidden', u'Kiellän ohjelmanumeroni videoinnin'),
]
START_TIME_LABEL = u'Alkuaika'

STATE_CHOICES = [
    (u'idea', u'Ideoitu sisäisesti'),
    (u'asked', u'Kysytty ohjelmanjärjestäjältä'),
    (u'offered', u'Ohjelmatarjous vastaanotettu'),
    (u'accepted', u'Hyväksytty'),
    (u'published', u'Julkaistu'),

    (u'cancelled', u'Peruutettu'),
    (u'rejected', u'Hylätty'),
]

STATE_CSS = dict(
    idea='label-default',
    asked='label-default',
    offered='label-default',
    accepted='label-primary',
    published='label-success',
    cancelled='label-danger',
    rejected='label-danger',
)


class Programme(models.Model, CsvExportMixin):
    category = models.ForeignKey('programme.Category', verbose_name=_(u'category'))

    title = models.CharField(
        max_length=1023,
        verbose_name=_(u'Title'),
        help_text=_(u'Make up a concise title for your programme. We reserve the right to edit the title.'),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_(u'Description'),
        help_text=_(u'This description is published in the web schedule and the programme booklet. The purpose of this description is to give the participant sufficient information to decide whether to take part or not and to market your programme to the participants. We reserve the right to edit the description.'),
    )
    room_requirements = models.TextField(
        blank=True,
        verbose_name=_(u'Requirements for the room'),
        help_text=u'How large an audience do you expect for your programme? What kind of a room do you wish for your programme?',
    )
    tech_requirements = models.TextField(
        blank=True,
        verbose_name=_(u'Tech requirements'),
        help_text=_(u'Do you need, for example, any of the following: computer, data projector, voice amplification, music playback capabilities, whiteboard, flipboard, chalkboard? The use of your own computer is only possible if agreed in advance.')
    )
    requested_time_slot = models.TextField(
        blank=True,
        verbose_name=_(u'Requested time slot'),
        help_text=_(u'At what time would you like to hold your programme? Are there other programme that you do not wish to co-incide with?'),
    )
    video_permission = models.CharField(
        max_length=15,
        choices=RECORDING_PERMISSION_CHOICES,
        default=RECORDING_PERMISSION_CHOICES[0][0],
        verbose_name=_(u'Recording permission'),
        help_text=_(u'May your programme be recorded and published in the Internet?'),
    )
    notes_from_host = models.TextField(
        blank=True,
        verbose_name=_(u'Anything else?'),
        help_text=_(u'If there is anything else you wish to say to the programme manager that is not covered by the above questions, please enter it here.'),
    )

    state = models.CharField(
        max_length=15,
        choices=STATE_CHOICES,
        default='accepted',
        verbose_name=_(u'State'),
        help_text=_(u'The programmes in the state "Published" will be visible to the general public, if the schedule has already been published.'),
    )

    start_time = models.DateTimeField(blank=True, null=True, verbose_name=START_TIME_LABEL)

    # denormalized
    end_time = models.DateTimeField(blank=True, null=True, verbose_name=_(u'Ending time'))

    length = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_(u'Length (minutes)'),
        help_text=_(u'In order to be displayed in the schedule, the programme must have a start time and a length and must be assigned into a room.'),
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_(u'Internal notes'),
        help_text=_(u'This field is normally only visible to the programme managers. However, should the programme host request a record of their own personal details, this field will be included in that record.'),
    )
    room = models.ForeignKey('programme.Room', blank=True, null=True, verbose_name=_(u'Room'))
    organizers = models.ManyToManyField('core.Person', through='ProgrammeRole', blank=True)
    tags = models.ManyToManyField('programme.Tag', blank=True, verbose_name=_(u'Tags'))

    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_(u'Created at'))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_(u'Updated at'))

    @property
    def event(self):
        return self.category.event

    @property
    def formatted_hosts(self):
        return u', '.join(p.display_name for p in self.organizers.all())

    @property
    def is_blank(self):
        return False

    def __unicode__(self):
        return self.title

    @property
    def css_classes(self):
        return self.category.style if self.category.style else ''

    @property
    def event(self):
        return self.category.event

    @property
    def is_active(self):
        return self.state not in ['rejected', 'cancelled']

    @property
    def is_rejected(self):
        return self.state == 'rejected'

    @property
    def is_cancelled(self):
        return self.state == 'cancelled'

    @property
    def is_published(self):
        return self.state == 'published'

    @classmethod
    def get_or_create_dummy(cls, title=u'Dummy program'):
        from .category import Category
        from .room import Room

        category, unused = Category.get_or_create_dummy()
        room, unused = Room.get_or_create_dummy()

        return cls.objects.get_or_create(
            title=title,
            defaults=dict(
                category=category,
                room=room,
            )
        )

    @property
    def formatted_start_time(self):
        return format_datetime(self.start_time) if self.start_time else ''

    @property
    def formatted_times(self):
        return u'{start_time} – {end_time}'.format(
            start_time=format_datetime(self.start_time),
            end_time=format_datetime(self.end_time),
        )

    # for json
    @property
    def category_title(self):
        return self.category.title

    @property
    def room_name(self):
        return self.room.name if self.room is not None else None

    @property
    def is_public(self):
        return self.state == 'published' and self.category is not None and self.category.public

    def as_json(self, format='default'):
        from core.utils import pick_attrs

        if format == 'default':
            return pick_attrs(self,
                'title',
                'description',
                'category_title',
                'formatted_hosts',
                'room_name',
                'length',
                'start_time',
                'is_public',
            )
        elif format == 'desucon':
            return pick_attrs(self,
                'title',
                'description',
                'start_time',
                'end_time',

                language='fi', # XXX hardcoded
                status=1 if self.is_public else 0,
                kind=self.category.slug,
                kind_display=self.category.title,
                identifier=u'p{id}'.format(id=self.id),
                location=self.room.name,
                location_slug=self.room.slug,
                presenter=self.formatted_hosts,
            )
        else:
            raise NotImplementedError(format)

    @property
    def state_css(self):
        return STATE_CSS[self.state]

    def save(self, *args, **kwargs):
        if self.start_time and self.length:
            self.end_time = self.start_time + timedelta(minutes=self.length)

        return super(Programme, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'programme')
        verbose_name_plural = _(u'programmes')
        ordering = ['start_time', 'room']