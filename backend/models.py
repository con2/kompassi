import datetime

from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=1023)
    style = models.CharField(max_length=15)
    notes = models.TextField(blank=True)

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


class Programme(models.Model):
    title = models.CharField(max_length=1023)
    description = models.TextField()
    start_time = models.DateTimeField()
    length = models.IntegerField()
    hilight = models.BooleanField()
    public = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    category = models.ForeignKey(Category)
    room = models.ForeignKey(Room)
    organizers = models.ManyToManyField(Person, through='ProgrammeRole')

    @property
    def end_time(self):
        return (self.start_time + datetime.timedelta(minutes=self.length))

    @property
    def formatted_hosts(self):
        return u', '.join(p.full_name for p in self.organizers.all())

    def __unicode__(self):
        return self.title

    @property
    def rowspan(self):
        return len(Programme.start_times(
            start_time__gte=self.start_time,
            start_time__lt=self.end_time,
            public=True
        ))

    @staticmethod
    def programmes_by_start_time():
        rooms = Room.objects.filter(public=True)

        results = []
        for start_time in Programme.start_times(public=True, room__public=True):
            cur_row = []
            results.append((start_time, cur_row))
            for room in rooms:
                try:
                    cur_row.append(Programme.objects.get(room=room, start_time=start_time, room__public=True, public=True))
                except Programme.DoesNotExist:
                    pass
                except Programme.MultipleObjectsReturned:
                    raise ValueError('Room {room} has multiple programs starting at {start_time}'.format(**locals()))

        return results

    @staticmethod
    def start_times(**conditions):
        return sorted(list(set(p.start_time for p in Programme.objects.filter(**conditions))))

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
