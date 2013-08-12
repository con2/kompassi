import datetime

from django.db import models


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


class Person(models.Model):
    first_name = models.CharField(max_length=1023)
    surname = models.CharField(max_length=1023)
    nick = models.CharField(blank=True, max_length=1023)
    email = models.EmailField(blank=True, max_length=254)
    phone = models.CharField(blank=True, max_length=255)
    anonymous = models.BooleanField()
    notes = models.TextField(blank=True)

    @property
    def full_name(self):
        if self.nick:
            return u'{0} "{1}" {2}'.format(
                self.first_name,
                self.nick,
                self.surname
            )
        else:
            return u'{0} {1}'.format(
                self.first_name,
                self.surname
            )

    @property
    def display_name(self):
        if self.anonymous:
            return self.nick
        else:
            return self.full_name

    def clean(self):
        if self.anonymous and not self.nick:
            from django.core.exceptions import ValidationError
            raise ValidationError('If real name is hidden a nick must be provided')

    def __unicode__(self):
        return self.full_name

    class Meta:
        ordering = ['surname']


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
    title = models.CharField(max_length=1023)
    description = models.TextField()
    start_time = models.DateTimeField()
    length = models.IntegerField()
    notes = models.TextField(blank=True)
    category = models.ForeignKey(Category)
    room = models.ForeignKey(Room)
    organizers = models.ManyToManyField(Person, through='ProgrammeRole')
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
    person = models.ForeignKey(Person)
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
        for start_time in self.start_times(room__public=True):
            cur_row = []
            results.append((start_time, cur_row))
            for room in self.rooms.filter(public=True):
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

    def start_times(self, **conditions):
        return sorted(list(set(p.start_time for p in Programme.objects.filter(room__in=self.public_rooms, **conditions))))

    @property
    def public_rooms(self):
        return self.rooms.filter(public=True)

    def rowspan(self, programme):
        return len(self.start_times(
            start_time__gte=programme.start_time,
            start_time__lt=programme.end_time
        ))


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