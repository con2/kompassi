# encoding: utf-8

from collections import namedtuple

from django.db import models
from django.conf import settings
from django.template.loader import render_to_string

from api.utils import JSONSchemaObject
from core.models import OneTimeCode
from core.utils import url


class Connection(models.Model):
    # no auto-increment
    id = models.IntegerField(
        primary_key=True,
        verbose_name='Desuprofiilin numero',
    )

    desuprofile_username = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Desuprofiilin käyttäjänimi',
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name='Käyttäjä',
    )

    def __str__(self):
        return self.user.username


class ConfirmationCode(OneTimeCode):
    desuprofile_id = models.IntegerField()

    desuprofile_username = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Desuprofiilin käyttäjänimi',
    )

    next_url = models.CharField(max_length=1023, blank=True, default='')

    def render_message_subject(self, request):
        return '{settings.KOMPASSI_INSTALLATION_NAME}: Desuprofiilin yhdistäminen'.format(settings=settings)

    def render_message_body(self, request):
        context = dict(
            link=request.build_absolute_uri(url('desuprofile_integration_confirmation_view', self.code))
        )

        return render_to_string('desuprofile_integration_confirmation_message.eml', context=context, request=request)


DesuprofileBase = namedtuple('Desuprofile', 'id username first_name last_name nickname email phone birth_date')
class Desuprofile(DesuprofileBase, JSONSchemaObject):
    schema = dict(
        type='object',
        properties=dict(
            id=dict(type='number'),
            username=dict(type='string', minLength=1, maxLength=150),
            first_name=dict(type='string', minLength=1),
            last_name=dict(type='string', minLength=1),
            nickname=dict(type='string', optional=True),
            email=dict(type='string', pattern=r'.+@.+\..+'),
            phone=dict(type='string'),

            # XXX
            birth_date=dict(anyOf=[
                dict(type='string', pattern=r'\d{4}-\d{1,2}-\d{1,2}'),
                dict(type='null'),
            ]),
        ),
        required=['id', 'username', 'first_name', 'last_name', 'email'],
    )


DesuprogrammeBase = namedtuple('Desuprogramme', 'identifier title description')
class Desuprogramme(DesuprogrammeBase, JSONSchemaObject):
    schema = dict(
        type='object',
        properties=dict(
            identifier=dict(type='string', minLength=1, maxLength=255, pattern=r'[a-z0-9-]+'),
            title=dict(type='string', minLength=1, maxLength=1023),
            description=dict(type='string'),
        ),
        required=['identifier', 'title', 'description'],
    )

    def get_or_create(self, category):
        from programme.models import Programme
        return Programme.objects.get_or_create(
                category=category,
                slug=self.identifier,
                defaults=dict(
                    title=self.title,
                    description=self.description,
                    state='accepted',
                    notes='Tuotu automaattisesti Desusaitilta',
                ),
            )
