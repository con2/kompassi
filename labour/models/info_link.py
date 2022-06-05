from django.db import models
from django.utils.translation import gettext_lazy as _


class InfoLink(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, verbose_name="Tapahtuma")
    group = models.ForeignKey(
        "auth.Group",
        on_delete=models.CASCADE,
        verbose_name="Ryhmä",
        help_text="Linkki näytetään vain tämän ryhmän jäsenille.",
    )

    url = models.CharField(
        max_length=255,
        verbose_name="Osoite",
        help_text="Muista aloittaa ulkoiset linkit <i>http://</i> tai <i>https://</i>.",
    )

    title = models.CharField(max_length=255, verbose_name="Teksti")

    class Meta:
        verbose_name = _("info link")
        verbose_name_plural = _("info links")

    def __str__(self):
        return self.title
