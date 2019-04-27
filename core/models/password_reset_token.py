from django.conf import settings
from django.db import models
from django.template.loader import render_to_string

from ..utils import change_user_password, url
from .one_time_code import OneTimeCode


class PasswordResetError(RuntimeError):
    pass


class PasswordResetToken(OneTimeCode):
    ip_address = models.CharField(max_length=45, blank=True) # IPv6

    def render_message_subject(self, request):
        return '{settings.KOMPASSI_INSTALLATION_NAME}: Salasanan vaihto'.format(settings=settings)

    def render_message_body(self, request):
        vars = dict(
            link=request.build_absolute_uri(url('core_password_reset_view', self.code))
        )

        return render_to_string('core_password_reset_message.eml', vars, request=request)

    @classmethod
    def reset_password(cls, code, new_password):
        try:
            code = cls.objects.get(code=code, state='valid')
        except cls.DoesNotExist:
            raise PasswordResetError('invalid_code')

        code.mark_used()

        user = code.person.user

        change_user_password(user, new_password=new_password)
