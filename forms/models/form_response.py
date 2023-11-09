import uuid

from django.conf import settings
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _


from .form import AbstractForm


class AbstractFormResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form_data = JSONField()

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ip_address = models.CharField(
        max_length=48,
        blank=True,
        default="",
        verbose_name=_("IP address"),
    )

    class Meta:
        abstract = True


class GlobalFormResponse(AbstractFormResponse):
    form = models.ForeignKey("forms.GlobalForm", on_delete=models.CASCADE)


class EventFormResponse(AbstractFormResponse):
    form = models.ForeignKey("forms.EventForm", on_delete=models.CASCADE)
