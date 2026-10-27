from datetime import timedelta

from django.conf import settings
from django.db import models, transaction
from django.template.loader import render_to_string
from django.utils.timezone import now

from kompassi.core.utils.cleanup import register_cleanup
from kompassi.graphql_api.language import SupportedLanguageCode
from kompassi.involvement.dumpers.section import section

from ..utils import url
from .one_time_code import OneTimeCode


class PasswordResetError(RuntimeError):
    pass


@register_cleanup(lambda qs: qs.filter(used_at__lt=now() - timedelta(days=30)))
class PasswordResetToken(OneTimeCode):
    ip_address = models.CharField(max_length=45, blank=True)  # IPv6

    def render_message_subject(self, request):
        return f"{settings.KOMPASSI_INSTALLATION_NAME}: Salasanan vaihto"

    def render_message_body(self, request):
        vars = dict(link=request.build_absolute_uri(url("core_password_reset_view", self.code)))

        return render_to_string("core_password_reset_message.eml", vars, request=request)

    @classmethod
    def reset_password(cls, code, new_password):
        with transaction.atomic():
            try:
                code = cls.objects.select_for_update(no_key=True).get(code=code, state="valid")
            except cls.DoesNotExist as dne:
                raise PasswordResetError("invalid_code") from dne

            code.mark_used()

            user = code.person.user
            user.set_password(new_password)
            user.save(update_fields=["password"])

            # the user's keypairs are encrypted with the user's password
            # so they can't be used if the user doesn't know their password
            user.keypairs.all().delete()

        return user

    def dump_own_data(self, language: SupportedLanguageCode) -> dict:
        # TODO how do we localize this?
        return section(
            title="Salasanan palautuskoodi",
            content={
                "IP-osoite": self.ip_address,
                **super().dump_own_data(language),
            },
        )
