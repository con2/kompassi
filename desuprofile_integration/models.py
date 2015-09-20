# encoding: utf-8

from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from core.models import OneTimeCode


class Connection(models.Model):
    # no auto-increment
    id = models.IntegerField(
        primary_key=True,
        verbose_name=u'Desuprofiilin numero',
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'Käyttäjä')


class ConfirmationError(RuntimeError):
    pass


class ConfirmationCode(OneTimeCode):
    desuprofile_json = models.TextField()

    @property
    def desuprofile(self):
        return json.loads(desuprofile_json)

    def render_message_subject(self, request):
        return u'{settings.KOMPASSI_INSTALLATION_NAME}: Desuprofiilin yhdistäminen'.format(settings=settings)

    def render_message_body(self, request):
        vars = dict(
            link=request.build_absolute_uri(url('desuprofile_integration_confirmation_view', self.code))
        )

        return render_to_string('desuprofile_integration_confirmation_message.eml', vars, context_instance=RequestContext(request, {}))
