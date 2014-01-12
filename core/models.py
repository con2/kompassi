# encoding: utf-8

from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils.dateformat import format as format_date
from django.conf import settings

from .helpers import validate_slug, SlugField

class Venue(models.Model):
    name = models.CharField(max_length=31)

    class Meta:
        verbose_name = u'Tapahtumapaikka'
        verbose_name_plural = u'Tapahtumapaikat'

    def __unicode__(self):
        return self.name


class Event(models.Model):
    slug = SlugField()
    name = models.CharField(max_length=31, verbose_name=u'Tapahtuman nimi')

    name_genitive = models.CharField(
        max_length=31,
        verbose_name=u'Tapahtuman nimi genetiivissä',
        help_text=u'Esimerkki: Susiconin',
    )

    name_illative = models.CharField(
        max_length=31,
        verbose_name=u'Tapahtuman nimi illatiivissä',
        help_text=u'Esimerkki: Susiconiin',
    )

    name_inessive = models.CharField(
        max_length=31,
        verbose_name=u'Tapahtuman nimi inessiivissä',
        help_text=u'Esimerkki: Susiconissa',
    )

    venue = models.ForeignKey(Venue,
        verbose_name=u'Tapahtumapaikka',
    )

    start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Alkamisaika',
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=u'Päättymisaika',
    )

    homepage_url = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=u'Tapahtuman kotisivu',
    )

    organization_name = models.CharField(
        blank=True,
        max_length=63,
        verbose_name=u'Järjestävä taho',
    )
    
    organization_url = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=u'Järjestävän tahon kotisivu'
    )

    class Meta:
        verbose_name = u'Tapahtuma'
        verbose_name_plural = u'Tapahtumat'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            for field, suffix in [
                ('name_genitive', 'in'),
                ('name_illative', 'iin'),
                ('name_inessive', 'issa')
            ]:
                if not getattr(self, field, None):
                    setattr(self, field, self.name + suffix)

        return super(Event, self).save(*args, **kwargs)

    @property
    def name_and_year(self):
        return u"{name} ({year})".format(
            name=self.name,
            year=self.start_time.year
        )


EMAIL_LENGTH = PHONE_NUMBER_LENGTH = 255
BIRTH_DATE_HELP_TEXT = u'Syntymäaika muodossa {0}'.format(
    format_date(date(1994, 2, 24), settings.DATE_FORMAT)
)


class Person(models.Model):
    first_name = models.CharField(max_length=1023, verbose_name=u'Etunimi')
    surname = models.CharField(max_length=1023, verbose_name=u'Sukunimi')
    nick = models.CharField(blank=True, max_length=1023, help_text='Lempi- tai kutsumanimi')
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=u'Syntymäaika',
        help_text=BIRTH_DATE_HELP_TEXT)

    email = models.EmailField(
        blank=True,
        max_length=EMAIL_LENGTH,
        verbose_name=u'Sähköpostiosoite'
    )
    
    phone = models.CharField(
        blank=True,
        max_length=PHONE_NUMBER_LENGTH,
        verbose_name=u'Puhelinnumero'
    )
    
    anonymous = models.BooleanField(
        default=False,
        verbose_name=u'Piilota etu- ja sukunimi',
        help_text=u'Jos valitset tämän, sinusta näytetään vain nick-kentässä asetettu '
            u'kutsumanimi. Etu- ja sukunimi on tällöinkin annettava, jolloin ne näkyvät '
            u'vain tapahtuman järjestäjille.'
    )

    notes = models.TextField(blank=True, verbose_name=u'Käsittelijän merkinnät')
    user = models.OneToOneField('auth.User', null=True, blank=True)

    class Meta:
        ordering = ['surname']
        verbose_name = u'Henkilö'
        verbose_name_plural = u'Henkilöt'

    def __unicode__(self):
        return self.full_name

    def clean(self):
        if self.anonymous and not self.nick:
            from django.core.exceptions import ValidationError
            raise ValidationError('If real name is hidden a nick must be provided')

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


__all__ = [
    'BIRTH_DATE_HELP_TEXT',
    'Event',
    'EMAIL_LENGTH',
    'Person',
    'PHONE_NUMBER_LENGTH',
    'Venue',
]
