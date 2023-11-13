import uuid
from functools import cached_property
from typing import Any

from django.conf import settings
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _


from ..utils import process_form_data


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

    form: Any

    def _process_form_data(self):
        return process_form_data(self.form, self.form_data)

    @cached_property
    def processed_form_data(self):
        return self._process_form_data()

    @property
    def values(self):
        return self.processed_form_data[0]

    @property
    def warnings(self):
        return self.processed_form_data[1]

    class Meta:
        abstract = True


class GlobalFormResponse(AbstractFormResponse):
    form = models.ForeignKey("forms.GlobalForm", on_delete=models.CASCADE)


class EventFormResponse(AbstractFormResponse):
    form = models.ForeignKey("forms.EventForm", on_delete=models.CASCADE)

    def _process_form_data(self):
        return process_form_data(self.form.enriched_fields, self.form_data)
