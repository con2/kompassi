import datetime

from django.db import models
from django.conf import settings

from .utils import window, next_full_hour, full_hours_between


ONE_HOUR = datetime.timedelta(hours=1)


class Category(models.Model):
    title = models.CharField(max_length=1023)
    style = models.CharField(max_length=15)
    notes = models.TextField(blank=True)
    public = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = "categories"


class Room(models.Model):
    name = models.CharField(max_length=1023)
    order = models.IntegerField(unique=True)
    public = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def programme_continues_at(self, the_time, **conditions):
        latest_programme = self.programme_set.filter(
            start_time__lt=the_time,
            **conditions
        ).order_by('-start_time')[:1]
        if latest_programme:
            return the_time < latest_programme[0].end_time
        else:
            return False

    class Meta:
        ordering = ['order']


class Role(models.Model):
    title = models.CharField(max_length=1023)
    require_contact_info = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=15)
    order = models.IntegerField(default=0)
    style = models.CharField(max_length=15, default='label-default')

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['order']

class Programme(models.Model):
    event = models.ForeignKey('core.Event', null=True, blank=True)
    title = models.CharField(max_length=1023)
    description = models.TextField()
    start_time = models.DateTimeField()
    length = models.IntegerField()
    notes = models.TextField(blank=True)
    category = models.ForeignKey(Category)
    room = models.ForeignKey(Room)
    organizers = models.ManyToManyField('core.Person', through='ProgrammeRole')
    tags = models.ManyToManyField(Tag, blank=True)

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

    class Meta:
        ordering = ['start_time', 'room']


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
                        start_time=start_time,
                        room__public=True
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
        result = settings.TIMETABLE_SPECIAL_TIMES[::]

        for (start_time, end_time) in settings.TIMETABLE_TIME_BLOCKS:
            cur = start_time
            while cur <= end_time:
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
    name = models.CharField(max_length=32)
    public = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    rooms = models.ManyToManyField(Room)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order']


class AllRoomsPseudoView(ViewMethodsMixin):
    def __init__(self):
        self.name = 'All rooms'
        self.public = True
        self.order = 0
        self.rooms = Room.objects.all()