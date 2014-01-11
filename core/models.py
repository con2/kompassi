# encoding: utf-8

from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=31)


class Event(models.Model):
    slug = models.CharField(max_length=31, primary_key=True)
    name = models.CharField(max_length=31)
    name_genitive = models.CharField(max_length=31)
    homepage_url = models.CharField(max_length=255)
    organization_name = models.CharField(max_length=63)
    organization_url = models.CharField(max_length=255)
    venue = models.ForeignKey(Venue)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    @property
    def name_and_year(self):
        return u"{name} ({year})".format(
            name=self.name,
            year=self.start_time.year
        )


EMAIL_LENGTH = PHONE_NUMBER_LENGTH = 255


class Person(models.Model):
    first_name = models.CharField(max_length=1023, verbose_name=u'Etunimi')
    surname = models.CharField(max_length=1023, verbose_name=u'Sukunimi')
    nick = models.CharField(blank=True, max_length=1023, help_text='Lempi- tai kutsumanimi')
    birth_date = models.DateField(null=True, blank=True, verbose_name=u'Syntymäaika')
    email = models.EmailField(blank=True, max_length=EMAIL_LENGTH, verbose_name=u'Sähköpostiosoite')
    phone = models.CharField(blank=True, max_length=PHONE_NUMBER_LENGTH, verbose_name=u'Puhelinnumero')
    anonymous = models.BooleanField(default=False, verbose_name=u'Piilota etu- ja sukunimi', help_text=u'Jos valitset tämän, sinusta näytetään vain nick-kentässä asetettu kutsumanimi. Etu- ja sukunimi on tällöinkin annettava, jolloin ne näkyvät vain tapahtuman järjestäjille.')
    notes = models.TextField(blank=True, verbose_name=u'Käsittelijän merkinnät')
    user = models.OneToOneField('auth.User', null=True, blank=True)

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

    @classmethod
    def create_dummy(cls):
        user, unused = User.objects.get_or_create(
            username='mahti',
            defaults=dict(
                first_name='Markku',
                last_name='Mahtinen',
                is_staff=True,
                is_superuser=True,
            ),
        )

        if not user.password:
            user.set_password('mahti')
            user.save()

        person, unused = cls.objects.get_or_create(
            user=user,
            defaults=dict(
                first_name=user.first_name,
                surname=user.last_name,
                nick='Mahti',
                birth_date=date(1984,1,1),
                email='mahti@example.com',
                phone='+358 50 555 1234'
            )
        )

        return person

    def __unicode__(self):
        return self.full_name

    class Meta:
        ordering = ['surname']


__all__ = [
    'Event',
    'EMAIL_LENGTH',
    'Person',
    'PHONE_NUMBER_LENGTH',
    'Venue',
]
