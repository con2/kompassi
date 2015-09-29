# encoding: utf-8

from collections import namedtuple

from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth import get_user_model

from jsonschema import validate

from api.utils import JSONSchemaObject
from core.models import OneTimeCode
from core.utils import url


class Connection(models.Model):
    # no auto-increment
    id = models.IntegerField(
        primary_key=True,
        verbose_name=u'Desuprofiilin numero',
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'Käyttäjä', unique=True)

    def __unicode__(self):
        return self.user.username


class ConfirmationCode(OneTimeCode):
    desuprofile_id = models.IntegerField()
    next_url = models.CharField(max_length=1023, blank=True, default='')

    def get_desuprofile(self):
        return json.loads(desuprofile_json)

    def render_message_subject(self, request):
        return u'{settings.KOMPASSI_INSTALLATION_NAME}: Desuprofiilin yhdistäminen'.format(settings=settings)

    def render_message_body(self, request):
        vars = dict(
            link=request.build_absolute_uri(url('desuprofile_integration_confirmation_view', self.code))
        )

        return render_to_string('desuprofile_integration_confirmation_message.eml', vars, context_instance=RequestContext(request, {}))


DesuprofileBase = namedtuple('Desuprofile', 'id username first_name last_name nickname email phone birth_date')
class Desuprofile(DesuprofileBase, JSONSchemaObject):
    schema = dict(
        type='object',
        properties=dict(
            id=dict(type='number'),
            username=dict(type='string', minLength=1),
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

