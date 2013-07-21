import datetime
from django.db import models

# Category
class Category(models.Model):
    title = models.CharField(max_length=1023)
    style = models.CharField(max_length=15)

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

    @property
    def full_name(self):
        return self.first_name + " " + self.surname

    @property
    def display_name(self):
        if self.anonymous:
            return self.nick
        elif self.nick:
            return self.first_name + " \"" + self.nick + "\" " + self.surname
        else:
            return self.full_name  

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.email or self.phone:
            raise ValidationError('Either e-mail address or phone number must be provided')
        if self.anonymous and not self.nick:
            raise ValidationError('If real name is hidden a nick must be provided')

    def __unicode__(self):
        return self.display_name

    class Meta:
        ordering = ['surname']


# Programme
class Programme(models.Model):
    title = models.CharField(max_length=1023)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    hilight = models.BooleanField()
    public = models.BooleanField(default=True)
    category = models.ForeignKey(Category)
    room = models.ForeignKey(Room)
    hosts = models.ManyToManyField(Person)

    @property
    def length(self):
        return (self.end_time - self.start_time)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['start_time','room']