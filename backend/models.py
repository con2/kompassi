import datetime
from django.db import models

# Category
class Category(models.Model):
    title = models.CharField(max_length=255)
    style = models.CharField(max_length=15)

    def __unicode__(self):
        return self.title


# Room
class Room(models.Model):
    name = models.CharField(max_length=255)
    order = models.IntegerField(unique=True)
    public = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order']


# Programme
class Programme(models.Model):
    title = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    hilight = models.BooleanField()
    public = models.BooleanField(default=True)
    category = models.ForeignKey(Category)
    room = models.ForeignKey(Room)

    @property
    def length(self):
        return (self.end_time - self.start_time)

    def __unicode__(self):
        return self.title
