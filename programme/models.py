# encoding: utf-8

import logging
import datetime
from datetime import timedelta
from pkg_resources import resource_string

from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.contrib import messages
from django.dispatch import receiver
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.csv_export import CsvExportMixin
from core.models import EventMetaBase, OneTimeCode
from core.utils import (
    alias_property,
    format_datetime,
    full_hours_between,
    get_postgresql_version_num,
    NONUNIQUE_SLUG_FIELD_PARAMS,
    slugify,
    url,
)

from .utils import window, next_full_hour


ONE_HOUR = datetime.timedelta(hours=1)
logger = logging.getLogger('kompassi')


HAVE_POSTGRESQL_TIME_RANGE_FUNCTIONS = get_postgresql_version_num() >= 90200


class ProgrammeEventMeta(EventMetaBase):
    public_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Ohjelmakartan julkaisuaika',
        help_text=u'Ohjelmakartta näkyy kansalle tästä eteenpäin.',
    )

    contact_email = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=u'yhteysosoite',
        help_text=u'Kaikki ohjelmajärjestelmän lähettämät sähköpostiviestit lähetetään tästä '
            u'osoitteesta, ja tämä osoite näytetään ohjelmanjärjestäjälle yhteysosoitteena. Muoto: Selite &lt;osoite@esimerkki.fi&gt;.',
    )

    def get_special_programmes(self, include_unpublished=False):
        schedule_rooms = Room.objects.filter(view__event=self.event).only('id')
        criteria = dict(category__event=self.event)
        if not include_unpublished:
            criteria.update(state='published')
        return Programme.objects.filter(**criteria).exclude(room__in=schedule_rooms)

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event

        event, unused = Event.get_or_create_dummy()
        admin_group, = cls.get_or_create_groups(event, ['admins'])

        return cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                public=True
            )
        )

    @property
    def is_public(self):
        return self.public_from is not None and now() > self.public_from

    public = alias_property('is_public')

class Category(models.Model):
    event = models.ForeignKey('core.Event')
    title = models.CharField(max_length=1023)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)
    style = models.CharField(max_length=15)
    notes = models.TextField(blank=True)
    public = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        unique_together = [('event', 'slug')]
        verbose_name = u'ohjelmaluokka'
        verbose_name_plural = u'ohjelmaluokat'

    @classmethod
    def get_or_create_dummy(cls):
        meta, unused = ProgrammeEventMeta.get_or_create_dummy()

        return cls.objects.get_or_create(
            event=meta.event,
            title='Dummy category',
            defaults=dict(
                style='dummy',
            )
        )


@receiver(pre_save, sender=Category)
def populate_category_slug(sender, instance, **kwargs):
    if instance.title and not instance.slug:
        instance.slug = slugify(instance.title)


class Room(models.Model):
    venue = models.ForeignKey('core.Venue')
    name = models.CharField(max_length=1023)
    order = models.IntegerField()
    notes = models.TextField(blank=True)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)

    def __unicode__(self):
        return self.name

    def programme_continues_at(self, the_time, **conditions):
        criteria = dict(
            start_time__lt=the_time,
            length__isnull=False,
            **conditions
        )

        latest_programme = self.programme_set.filter(**criteria).order_by('-start_time')[:1]
        if latest_programme:
            return the_time < latest_programme[0].end_time
        else:
            return False

    class Meta:
        ordering = ['venue', 'order']
        verbose_name = u'tila'
        verbose_name_plural = u'tilat'
        unique_together = [
            ('venue', 'order'),
            ('venue', 'slug'),
        ]

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Venue
        venue, unused = Venue.get_or_create_dummy()
        return cls.objects.get_or_create(
            venue=venue,
            name=u'Dummy room',
            defaults=dict(
                order=0,
            )
        )


@receiver(pre_save, sender=Room)
def populate_room_slug(sender, instance, **kwargs):
    if instance.name and not instance.slug:
        instance.slug = slugify(instance.name)


class Role(models.Model):
    title = models.CharField(max_length=1023)
    require_contact_info = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'rooli'
        verbose_name_plural = u'roolit'
        ordering = ['title']

    @classmethod
    def get_or_create_dummy(cls):
        return cls.objects.get_or_create(
            title=u'Overbaron',
            require_contact_info=False
        )


class Tag(models.Model):
    event = models.ForeignKey('core.Event')
    title = models.CharField(max_length=63)
    order = models.IntegerField(default=0)
    style = models.CharField(max_length=15, default='label-default')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'tägi'
        verbose_name_plural = u'tägit'
        ordering = ['order']


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
    category = models.ForeignKey(Category, verbose_name=u'Ohjelmaluokka')

    title = models.CharField(
        max_length=1023,
        verbose_name=u'Otsikko',
        help_text=u'Keksi ohjelmanumerollesi lyhyt ja ytimekäs otsikko ohjelmakarttaa sekä ohjelmalehteä varten. Tracon varaa oikeuden muuttaa otsikkoa.',
    )
    description = models.TextField(
        blank=True,
        verbose_name=u'Ohjelmanumeron kuvaus',
        help_text=u'Ohjelmakuvaus näkyy web-ohjelmakartassa sekä ohjelmalehdessä. Ohjelmakuvauksen tarkoitus on antaa kävijälle riittävät tiedot päättää, osallistuako ohjelmaasi, ja markkinoida ohjelmaasi kävijöille. Tracon varaa oikeuden editoida kuvausta.',
    )
    room_requirements = models.TextField(
        blank=True,
        verbose_name=u'Tilatarpeet',
        help_text=u'Kuinka paljon odotat ohjelmanumerosi vetävän yleisöä? Minkälaista salia toivot ohjelmanumerosi käyttöön?',
    )
    tech_requirements = models.TextField(
        blank=True,
        verbose_name=u'Tekniikkatarpeet',
        help_text=u'Tarvitsetko ohjelmasi pitämiseen esimerkiksi tietokonetta, videotykkiä, luentoäänentoistoa, musiikkiäänentoistoa, tussi-, fläppi- tai liitutaulua tai muita erityisvälineitä? Oman tietokoneen käyttö on mahdollista vain, jos siitä on sovittu etukäteen.',
    )
    requested_time_slot = models.TextField(
        blank=True,
        verbose_name=u'Aikatoiveet',
        help_text=u'Mihin aikaan haluaisit pitää ohjelmanumerosi? Minkä ohjelmanumeroiden kanssa et halua olla päällekäin?'
    )
    video_permission = models.CharField(
        max_length=15,
        choices=RECORDING_PERMISSION_CHOICES,
        default=RECORDING_PERMISSION_CHOICES[0][0],
        verbose_name=u'Videointilupa',
        help_text=u'Saako luentosi videoida ja julkaista Internetissä?',
    )
    notes_from_host = models.TextField(
        blank=True,
        verbose_name=u'Vapaamuotoiset terveiset ohjelmavastaaville',
        help_text=u'Jos haluat sanoa ohjelmanumeroosi liittyen jotain, mikä ei sovi mihinkään yllä olevista kentistä, käytä tätä kenttää.',
    )

    state = models.CharField(
        max_length=15,
        choices=STATE_CHOICES,
        default='accepted',
        verbose_name=u'Ohjelmanumeron tila',
        help_text=u'Tilassa "Julkaistu" olevat ohjelmat näkyvät ohjelmakartassa, jos ohjelmakartta on julkinen.',
    )
    start_time = models.DateTimeField(blank=True, null=True, verbose_name=START_TIME_LABEL)

    # denormalized
    end_time = models.DateTimeField(blank=True, null=True, verbose_name=u'Päättymisaika')

    length = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=u'Kesto (minuuttia)',
        help_text=u'Ohjelmalla tulee olla tila, alkuaika ja kesto, jotta se näkyisi ohjelmakartassa.'
    )

    notes = models.TextField(
        blank=True,
        verbose_name=u'Ohjelmavastaavan muistiinpanot',
        help_text=u'Tämä kenttä ei normaalisti näy ohjelman järjestäjälle, mutta jos henkilö '
            u'pyytää henkilörekisteriotetta, kentän arvo on siihen sisällytettävä.'
    )
    room = models.ForeignKey(Room, blank=True, null=True, verbose_name=u'Tila')
    organizers = models.ManyToManyField('core.Person', through='ProgrammeRole', blank=True)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=u'Tägit')

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

    def send_edit_codes(self, request):
        for person in self.organizers.all():
            if not person.email:
                continue

            code, created = ProgrammeEditToken.objects.get_or_create(
                person=person,
                programme=self,
            )

            code.send(request)

    class Meta:
        verbose_name = u'ohjelmanumero'
        verbose_name_plural = u'ohjelmanumerot'
        ordering = ['start_time', 'room']

    @classmethod
    def get_or_create_dummy(cls, title=u'Dummy program'):
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
                'public',
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

    def get_overlapping_programmes(self):
        if any((
            self.id is None,
            self.room is None,
            self.start_time is None,
            self.length is None,
        )):
            return Programme.objects.none()
        elif HAVE_POSTGRESQL_TIME_RANGE_FUNCTIONS:
            return Programme.objects.raw(
                resource_string(__name__, 'sql/overlapping_programmes.sql'),
                (
                    self.category.event.id,
                    self.id,
                    self.room.id,
                    self.start_time,
                    self.end_time,
                )
            )
        else:
            logger.warn('DB engine not PostgreSQL >= 9.2. Cannot detect overlapping programmes.')
            return Programme.objects.none()


class ProgrammeRole(models.Model):
    person = models.ForeignKey('core.Person')
    programme = models.ForeignKey(Programme)
    role = models.ForeignKey(Role)

    def clean(self):
        if self.role.require_contact_info and not (self.person.email or self.person.phone):
            from django.core.exceptions import ValidationError
            raise ValidationError('Contacts of this type require some contact info')

    def __unicode__(self):
        return self.role.title

    class Meta:
        verbose_name = u'ohjelmanpitäjän rooli'
        verbose_name_plural = u'ohjelmanpitäjien roolit'

    @classmethod
    def get_or_create_dummy(cls, programme=None):
        from core.models import Person

        person, unused = Person.get_or_create_dummy()
        role, unused = Role.get_or_create_dummy()

        if programme is None:
            programme, unused = Programme.get_or_create_dummy()

        ProgrammeRole.objects.get_or_create(
            person=person,
            programme=programme,
            role=role,
        )


class ViewMethodsMixin(object):
    @property
    def programmes_by_start_time(self):
        return self.get_programmes_by_start_time()

    def get_programmes_by_start_time(self, include_unpublished=False, request=None):
        results = []
        prev_start_time = None
        cont_criteria = dict() if include_unpublished else dict(state='published')

        for start_time in self.start_times():
            cur_row = []
            criteria = dict(
                category__event=self.event,
                start_time=start_time,
                length__isnull=False,
            )

            if not include_unpublished:
                criteria.update(state='published')

            incontinuity = prev_start_time and (start_time - prev_start_time > ONE_HOUR)
            incontinuity = 'incontinuity' if incontinuity else ''
            prev_start_time = start_time

            results.append((start_time, incontinuity, cur_row))
            for room in self.rooms.all():
                programmes = room.programme_set.filter(**criteria)
                num_programmes = programmes.count()
                if num_programmes == 0:
                    if room.programme_continues_at(start_time, **cont_criteria):
                        # programme still continues, handled by rowspan
                        pass
                    else:
                        # there is no (visible) programme in the room at start_time, insert a blank
                        cur_row.append((None, None))
                else:
                    if programmes.count() > 1:
                        logger.warn('Room %s has multiple programs starting at %s', room, start_time)

                        if (
                            request is not None and
                            self.event.programme_event_meta.is_user_admin(request.user)
                        ):
                            messages.warning(request,
                                u'Tilassa {room} on päällekkäisiä ohjelmanumeroita kello {start_time}'.format(
                                    room=room,
                                    start_time=format_datetime(start_time.astimezone(tzlocal())),
                                )
                            )

                    programme = programmes.first()

                    rowspan = self.rowspan(programme)
                    cur_row.append((programme, rowspan))

        return results

    def start_times(self, programme=None):
        result = [t.start_time for t in SpecialStartTime.objects.filter(event=self.event)]

        for time_block in TimeBlock.objects.filter(event=self.event):
            cur = time_block.start_time
            while cur <= time_block.end_time:
                result.append(cur)
                cur += ONE_HOUR

        if programme:
            result = [
                i for i in result if
                    programme.start_time <= i < programme.end_time
            ]

        return sorted(set(result))

    def rowspan(self, programme):
        return len(self.start_times(programme=programme))


class View(models.Model, ViewMethodsMixin):
    event = models.ForeignKey('core.Event')
    name = models.CharField(max_length=32)
    public = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    rooms = models.ManyToManyField(Room)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'ohjelmakarttanäkymä'
        verbose_name_plural = u'ohjelmakarttanäkymät'
        ordering = ['event', 'order']


class AllRoomsPseudoView(ViewMethodsMixin):
    def __init__(self, event):
        self.name = 'All rooms'
        self.public = True
        self.order = 0
        self.rooms = Room.objects.filter(venue=event.venue, view__event=event)
        self.event = event


# abuses OneTimeCode as these aren't "one-time"
class ProgrammeEditToken(OneTimeCode):
    programme = models.ForeignKey(Programme)

    def render_message_subject(self, request):
        return u'{self.programme.event.name}: Ilmoita ohjelmanumerosi tiedot'.format(self=self)

    def render_message_body(self, request):
        from django.template import RequestContext
        from django.template.loader import render_to_string

        vars = dict(
            code=self,
            link=request.build_absolute_uri(url('programme_self_service_view', self.programme.event.slug, self.code))
        )

        return render_to_string('programme_self_service_message.eml', vars, context_instance=RequestContext(request, {}))

    def send(self, *args, **kwargs):
        kwargs.setdefault('from_email', self.programme.event.programme_event_meta.contact_email)
        super(ProgrammeEditToken, self).send(*args, **kwargs)


class TimeBlock(models.Model):
    event = models.ForeignKey('core.event')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class SpecialStartTime(models.Model):
    event = models.ForeignKey('core.event', verbose_name=u'tapahtuma')
    start_time = models.DateTimeField(verbose_name=u'alkuaika')

    def __unicode__(self):
        from core.utils import format_datetime
        return format_datetime(self.start_time) if self.start_time else u'None'

    class Meta:
        verbose_name = u'poikkeava alkuaika'
        verbose_name_plural = u'poikkeavat alkuajat'
        ordering = ['event', 'start_time']
        unique_together = [
            ('event', 'start_time'),
        ]


__all__ = [
    'AllRoomsPseudoView',
    'Category',
    'Programme',
    'ProgrammeEditToken',
    'ProgrammeEventMeta',
    'ProgrammeRole',
    'Role',
    'Room',
    'Tag',
    'View',
    'ViewMethodsMixin',
]
