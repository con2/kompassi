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
    (u'public', _(u'My programme may be recorded and published')),
    (u'private', _(u'I forbid publishing my programme, but it may be recorded for archiving purposes')),
    (u'forbidden', _(u'I forbid recording my programme altogether')),
]
START_TIME_LABEL = _(u'Starting time')

STATE_CHOICES = [
    (u'idea', _(u'Internal programme idea')),
    (u'asked', _(u'Asked from the host')),
    (u'offered', _(u'Offer received')),
    (u'accepted', _(u'Accepted')),
    (u'published', _(u'Published')),

    (u'cancelled', _(u'Cancelled')),
    (u'rejected', _(u'Rejected')),
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

COMPUTER_CHOICES = [
    (u'con', _(u'Laptop provided by the event')),
    (u'pc', _(u'Own laptop – PC')),
    (u'mac', _(u'Own laptop – Mac')),
    (u'none', _(u'No computer required')),
]

TRISTATE_CHOICES = [
    ('yes', _(u'Yes')),
    ('no', _(u'No')),
    ('notsure', _(u'Not sure')),
]

TRISTATE_FIELD_PARAMS = dict(
    choices=TRISTATE_CHOICES,
    max_length=max(len(key) for (key, label) in TRISTATE_CHOICES),
)

ENCUMBERED_CONTENT_CHOICES = [
    ('yes', _(u'My programme contains copyright-encumbered audio or video')),
    ('no', _(u'My programme does not contain copyright-encumbered audio or video')),
    ('notsure', _(u'I\'m not sure whether my programme contains copyright-encumbered content or not')),
]

PHOTOGRAPHY_CHOICES = [
    ('please', _(u'Please photograph my programme')),
    ('okay', _(u'It\'s OK to photograph my programme')),
    ('nope', _(u'Please do not photograph my programme')),
]


class Programme(models.Model, CsvExportMixin):
    category = models.ForeignKey('programme.Category', verbose_name=_(u'category'))
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)

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

    use_audio = models.CharField(
        default='no',
        verbose_name=_(u'Audio playback'),
        help_text=_(u'Will you play audio in your programme?'),
        **TRISTATE_FIELD_PARAMS
    )

    use_video = models.CharField(
        default='no',
        verbose_name=_(u'Video playback'),
        help_text=_(u'Will you play video in your programme?'),
        **TRISTATE_FIELD_PARAMS
    )

    number_of_microphones = models.IntegerField(
        default=1,
        verbose_name=_(u'Microphones'),
        help_text=_(u'How many microphones do you require?'),
        choices=[
            (0, '0'),
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (99, _(u'More than five – Please elaborate on your needs in the "Other tech requirements" field.')),
        ],
    )

    computer = models.CharField(
        default='con',
        choices=COMPUTER_CHOICES,
        max_length=max(len(key) for (key, label) in COMPUTER_CHOICES),
        verbose_name=_(u'Computer use'),
        help_text=_(u'What kind of a computer do you wish to use? The use of your own computer is only possible if agreed in advance.'),
    )

    tech_requirements = models.TextField(
        blank=True,
        verbose_name=_(u'Other tech requirements'),
        help_text=_(u'Do you have tech requirements that are not covered by the previous questions?')
    )

    room_requirements = models.TextField(
        blank=True,
        verbose_name=_(u'Room requirements'),
        help_text=u'How large an audience do you expect for your programme? What kind of a room do you wish for your programme?',
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

    encumbered_content = models.CharField(
        default='no',
        max_length=max(len(key) for (key, label) in ENCUMBERED_CONTENT_CHOICES),
        choices=ENCUMBERED_CONTENT_CHOICES,
        verbose_name=_(u'Encumbered content'),
        help_text=_(u'Encumbered content cannot be displayed on our YouTube channel. Encumbered content will be edited out of video recordings.'),
    )

    photography = models.CharField(
        default='okay',
        max_length=max(len(key) for (key, label) in PHOTOGRAPHY_CHOICES),
        choices=PHOTOGRAPHY_CHOICES,
        verbose_name=_(u'Photography of your prorgmme'),
        help_text=_(u'Our official photographers will try to cover all programmes whose hosts request their programmes to be photographed.'),
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
        from .programme_role import ProgrammeRole
        from .freeform_organizer import FreeformOrganizer

        parts = [f.text for f in FreeformOrganizer.objects.filter(programme=self)]

        public_programme_roles = ProgrammeRole.objects.filter(
            programme=self,
            role__is_public=True
        ).select_related('person')

        parts.extend(pr.person.display_name for pr in public_programme_roles)

        return u', '.join(parts)

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
    def get_or_create_dummy(cls, title=u'Dummy program', state='published'):
        from .category import Category
        from .room import Room

        category, unused = Category.get_or_create_dummy()
        room, unused = Room.get_or_create_dummy()

        return cls.objects.get_or_create(
            title=title,
            defaults=dict(
                category=category,
                room=room,
                state=state,
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

        if self.title and not self.slug:
            self.slug = slugify(self.title)

        return super(Programme, self).save(*args, **kwargs)

    def apply_state(self):
        self.apply_state_create_badges()

    def apply_state_create_badges(self, deleted_programme_roles=[]):
        if 'badges' not in settings.INSTALLED_APPS:
            return

        if self.event.badges_event_meta is None:
            return

        from badges.models import Badge

        for person in self.organizers.all():
            Badge.ensure(event=self.event, person=person)

        for deleted_programme_role in deleted_programme_roles:
            Badge.ensure(event=self.event, person=deleted_programme_role.person)

    class Meta:
        verbose_name = _(u'programme')
        verbose_name_plural = _(u'programmes')
        ordering = ['start_time', 'room']
        index_together = [('category', 'state')]
        # unique_together = [('category', 'slug')]