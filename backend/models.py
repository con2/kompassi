import datetime
from django.db import models

# Category
class Category(models.Model):
    title = models.CharField(max_length=1023)
    style = models.CharField(max_length=15)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = "categories"


# Room
class Room(models.Model):
    name = models.CharField(max_length=1023)
    order = models.IntegerField(unique=True)
    public = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order']


# Person
class Person(models.Model):
    first_name = models.CharField(max_length=1023)
    surname = models.CharField(max_length=1023)
    nick = models.CharField(blank=True,max_length=1023)
    email = models.EmailField(blank=True,max_length=254)
    phone = models.CharField(blank=True,max_length=255)
    anonymous = models.BooleanField()
    notes = models.TextField(blank=True)

    @property
    def full_name(self):
        if self.nick:
            return self.first_name + " \"" + self.nick + "\" " + self.surname
        else:
            return self.first_name + " " + self.surname

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


# Role
class Role(models.Model):
    title = models.CharField(max_length=1023)
    require_contact_info = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
    

# Programme
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
    organizers = models.ManyToManyField(Person, through='ProgramRole')

    @property
    def end_time(self):
        return (self.start_time + datetime.timedelta(minutes = self.length))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['start_time','room']


# ProgramRole
class ProgramRole(models.Model):
    person = models.ForeignKey(Person)
    programme = models.ForeignKey(Programme)
    role = models.ForeignKey(Role)

    def __unicode__(self):
        return self.role.title