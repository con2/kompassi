import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class SlackError(RuntimeError):
    pass


class SlackAccess(models.Model):
    privilege = models.OneToOneField(
        "access.Privilege",
        on_delete=models.CASCADE,
        related_name="slack_access",
    )
    team_name = models.CharField(
        max_length=255,
        verbose_name="Slack-yhteisön nimi",
    )
    invite_link = models.CharField(
        max_length=255,
        default="https://example.com",
        verbose_name="Kutsulinkki",
        help_text='Saat kutsulinkin Slackin sovelluksesta vasemman yläkulman valikosta valitsemalla "Invite people to …". Valitse "Edit link settings", aseta kutsulinkin kelpoisuusajaksi ikuinen ja poista ruksi ruudusta "Send me Slacbot message…".',
    )

    def __str__(self):
        return self.team_name

    @classmethod
    def get_or_create_dummy(cls):
        from .privilege import Privilege

        privilege, unused = Privilege.get_or_create_dummy("slack")

        return cls.objects.get_or_create(
            privilege=privilege,
            defaults=dict(
                team_name="test",
            ),
        )

    class Meta:
        verbose_name = _("Slack invite automation")
        verbose_name_plural = _("Slack invite automations")
