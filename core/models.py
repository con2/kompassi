from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=31)


class Event(models.Model):
    slug = models.CharField(max_length=31, unique=True)
    name = models.CharField(max_length=31)
    venue = models.ForeignKey(Venue)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    @property
    def name_and_year(self):
        return u"{name} ({year})".format(
            name=self.name,
            year=self.start_time.year
        )


class Person(models.Model):
    first_name = models.CharField(max_length=1023)
    surname = models.CharField(max_length=1023)
    nick = models.CharField(blank=True, max_length=1023)
    email = models.EmailField(blank=True, max_length=255)
    phone = models.CharField(blank=True, max_length=255)
    anonymous = models.BooleanField()
    notes = models.TextField(blank=True)
    user = models.ForeignKey('auth.User', null=True, blank=True)

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