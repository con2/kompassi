import logging

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.utils import SLUG_FIELD_PARAMS

logger = logging.getLogger('kompassi')


class Form(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_standalone = models.BooleanField(
        default=True,
        verbose_name=_('Stand-alone'),
        help_text=_(
            'Stand-alone forms can be used via the generic form views whereas '
            'non-stand-alone forms can only be accessed from some other facility.'
        ),
    )

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fields = JSONField()

    def __str__(self):
        return self.title
