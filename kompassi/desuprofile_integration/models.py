from collections import namedtuple
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.utils.timezone import now

from kompassi.api.utils import JSONSchemaObject
from kompassi.core.models import OneTimeCode
from kompassi.core.utils import url
from kompassi.core.utils.cleanup import register_cleanup

DESUPROFILE_USERNAME_MAX_LENGTH = 150


class Connection(models.Model):
    # no auto-increment
    id = models.IntegerField(
        primary_key=True,
        verbose_name="Desuprofiilin numero",
    )

    desuprofile_username = models.CharField(
        max_length=DESUPROFILE_USERNAME_MAX_LENGTH,
        blank=True,
        verbose_name="Desuprofiilin käyttäjänimi",
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Käyttäjä",
    )

    def __str__(self):
        return self.user.username


@register_cleanup(lambda qs: qs.filter(used_at__lt=now() - timedelta(days=30)))
class ConfirmationCode(OneTimeCode):
    desuprofile_id = models.IntegerField()

    desuprofile_username = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Desuprofiilin käyttäjänimi",
    )

    next_url = models.CharField(max_length=1023, blank=True, default="")

    user: User

    def render_message_subject(self, request):
        return f"{settings.KOMPASSI_INSTALLATION_NAME}: Desuprofiilin yhdistäminen"

    def render_message_body(self, request):
        context = dict(link=request.build_absolute_uri(url("desuprofile_integration_confirmation_view", self.code)))

        return render_to_string("desuprofile_integration_confirmation_message.eml", context=context, request=request)


DesuprofileBase = namedtuple("Desuprofile", "id username first_name last_name nickname email phone birth_date")


class Desuprofile(DesuprofileBase, JSONSchemaObject):
    schema = dict(
        type="object",
        properties=dict(
            id=dict(type="number"),
            username=dict(type="string", minLength=1, maxLength=150),
            first_name=dict(type="string", minLength=1),
            last_name=dict(type="string", minLength=1),
            nickname=dict(type="string", optional=True),
            email=dict(type="string", pattern=r".+@.+\..+"),
            phone=dict(type="string"),
            # XXX
            birth_date=dict(
                anyOf=[
                    dict(type="string", pattern=r"\d{4}-\d{1,2}-\d{1,2}"),
                    dict(type="null"),
                ]
            ),
        ),
        required=["id", "username", "first_name", "last_name", "email"],
    )


DesuprogrammeFeedbackBase = namedtuple("DesuprogrammeFeedback", "feedback desucon_username anonymous ip_address")


class DesuprogrammeFeedback(DesuprogrammeFeedbackBase, JSONSchemaObject):
    schema = dict(
        type="object",
        properties=dict(
            feedback=dict(type="string", minLength=1),
            desucon_username=dict(type="string", maxLength=DESUPROFILE_USERNAME_MAX_LENGTH),
            anonymous=dict(type="boolean"),
            ip_address=dict(
                anyOf=[
                    dict(type="string", format="ipv4"),
                    dict(type="string", format="ipv6"),
                ]
            ),
        ),
        required=["feedback"],
    )

    def save(self, programme):
        from kompassi.zombies.programme.models import ProgrammeFeedback

        connection = Connection.objects.filter(desuprofile_username=self.desucon_username).first()
        attrs = dict()

        # XXX desusaitti is targeted by SQLi injections detected by this
        if "\0" in self.feedback:
            raise ValidationError("Feedback contains NUL byte")

        # XXX this must die
        if self.desucon_username is not None:
            attrs["author_external_username"] = self.desucon_username
        if self.ip_address is not None:
            attrs["author_ip_address"] = self.ip_address
        if connection:
            attrs["author"] = connection.user.person  # type: ignore
        if self.anonymous is not None:
            attrs["is_anonymous"] = self.anonymous

        return ProgrammeFeedback.objects.create(
            programme=programme,
            feedback=self.feedback,
            **attrs,
        )
