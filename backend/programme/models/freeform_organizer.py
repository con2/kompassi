from django.db import models
from django.utils.translation import gettext_lazy as _


class FreeformOrganizer(models.Model):
    """
    Not all programme-organizing entities are natural Persons. Programme might be attributed to,
    for example, companies, non-profit associations or informal groups of people such as convention
    committees.
    """

    programme = models.ForeignKey(
        "programme.Programme",
        on_delete=models.CASCADE,
        verbose_name=_("Programme"),
        related_name="freeform_organizers",
    )

    text = models.CharField(
        max_length=255,
        verbose_name=_("Text"),
        help_text=_("This text will be shown as-is in the schedule"),
    )

    def __str__(self):
        return f"{self.text} ({self.programme})"

    class Meta:
        verbose_name = _("freeform organizer")
        verbose_name_plural = _("freeform organizers")
