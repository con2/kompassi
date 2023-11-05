import logging

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import SLUG_FIELD_PARAMS, NONUNIQUE_SLUG_FIELD_PARAMS
from django.db.models import JSONField


logger = logging.getLogger("kompassi")

LAYOUT_CHOICES = [
    ("horizontal", _("Horizontal")),
    ("vertical", _("Vertical")),
]


class AbstractForm(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    active = models.BooleanField(default=True)
    standalone = models.BooleanField(
        default=True,
        verbose_name=_("Stand-alone"),
        help_text=_(
            "Stand-alone forms can be used via the generic form views whereas "
            "non-stand-alone forms can only be accessed from some other facility."
        ),
    )
    layout = models.CharField(
        verbose_name=_("Layout"),
        choices=LAYOUT_CHOICES,
        max_length=max(len(c) for (c, t) in LAYOUT_CHOICES),
        default=LAYOUT_CHOICES[0][0],
    )
    login_required = models.BooleanField(
        default=False,
        verbose_name=_("Login required"),
        help_text=_(
            "This switch only takes effect in a stand-alone context. In non-stand-alone "
            "contexts the use case will direct whether or not login is required."
        ),
    )

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fields = JSONField()

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class GlobalForm(AbstractForm):
    slug = models.CharField(**SLUG_FIELD_PARAMS)  # type: ignore


class EventForm(AbstractForm):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="forms")
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    class Meta:
        unique_together = [("event", "slug")]
