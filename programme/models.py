# encoding: utf-8

import datetime

from django.db import models
from django.conf import settings

from core.csv_export import CsvExportMixin
from core.models import EventMetaBase, OneTimeCode
from core.utils import url

from .utils import window, next_full_hour, full_hours_between


ONE_HOUR = datetime.timedelta(hours=1)


class ProgrammeEventMeta(EventMetaBase):
    public = models.BooleanField(default=True)

    contact_email = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=u'yhteysosoite',
        help_text=u'Kaikki ohjelmajärjestelmän lähettämät sähköpostiviestit lähetetään tästä '
            u'osoitteesta, ja tämä osoite näytetään ohjelmanjärjestäjälle yhteysosoitteena. Muoto: Selite &lt;osoite@esimerkki.fi&gt;.',
    )

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event

        event, unused = Event.get_or_create_dummy()
        admin_group, unused = cls.get_or_create_group(event, 'admins')

        return cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=admin_group,
                public=True
            )
        )


class Category(models.Model):
    event = models.ForeignKey('core.Event')
    title = models.CharField(max_length=1023)
    style = models.CharField(max_length=15)
    notes = models.TextField(blank=True)
    public = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
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


class Room(models.Model):
    venue = models.ForeignKey('core.Venue')
    name = models.CharField(max_length=1023)
    order = models.IntegerField()
    public = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def programme_continues_at(self, the_time, **conditions):
        latest_programme = self.programme_set.filter(
            start_time__lt=the_time,
            length__isnull=False,
            **conditions
        ).order_by('-start_time')[:1]
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
    title = models.CharField(max_length=15)
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

    start_time = models.DateTimeField(blank=True, null=True, verbose_name=START_TIME_LABEL)
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
    def end_time(self):
        return (self.start_time + datetime.timedelta(minutes=self.length))

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
    def public(self):
        return self.category.public

    @property
    def event(self):
        return self.category.event

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
    def get_or_create_dummy(cls):
        category, unused = Category.get_or_create_dummy()
        room, unused = Room.get_or_create_dummy()

        return cls.objects.get_or_create(
            title=u'Dummy program',
            defaults=dict(
                category=category,
                room=room,
            )
        )

    @property
    def formatted_start_time(self):
        from core.utils import format_datetime
        return format_datetime(self.start_time) if self.start_time else ''


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
    def get_or_create_dummy(cls):
        from core.models import Person

        person, unused = Person.get_or_create_dummy()
        role, unused = Role.get_or_create_dummy()
        programme, unused = Programme.get_or_create_dummy()

        ProgrammeRole.objects.get_or_create(
            person=person,
            programme=programme,
            role=role,
        )



class ViewMethodsMixin(object):
    @property
    def programmes_by_start_time(self):
        results = []
        prev_start_time = None

        for start_time in self.start_times():
            cur_row = []

            incontinuity = prev_start_time and (start_time - prev_start_time > ONE_HOUR)
            incontinuity = 'incontinuity' if incontinuity else ''
            prev_start_time = start_time

            results.append((start_time, incontinuity, cur_row))
            for room in self.public_rooms:
                try:
                    programme = room.programme_set.get(
                        category__event=self.event,
                        start_time=start_time,
                        room__public=True,
                        length__isnull=False,
                    )
                    rowspan = self.rowspan(programme)
                    cur_row.append((programme, rowspan))
                except Programme.DoesNotExist:
                    if room.programme_continues_at(start_time):
                        # programme still continues, handled by rowspan
                        pass
                    else:
                        # there is no (visible) programme in the room at start_time, insert a blank
                        cur_row.append((None, None))
                except Programme.MultipleObjectsReturned:
                    raise ValueError('Room {room} has multiple programs starting at {start_time}'.format(**locals()))

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

    @property
    def public_rooms(self):
        return self.rooms.filter(public=True)

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
        self.rooms = Room.objects.filter(venue=event.venue)
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
