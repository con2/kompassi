import uuid
from functools import cached_property
from typing import Any, TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from ..utils import FieldWarning


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
        from ..utils import process_form_data

        return process_form_data(self.form.validated_fields, self.form_data)

    @cached_property
    def processed_form_data(self):
        return self._process_form_data()

    @property
    def values(self) -> dict[str, Any]:
        return self.processed_form_data[0]

    @property
    def warnings(self) -> dict[str, list["FieldWarning"]]:
        return self.processed_form_data[1]

    class Meta:
        abstract = True


class GlobalFormResponse(AbstractFormResponse):
    form = models.ForeignKey("forms.GlobalForm", on_delete=models.CASCADE, related_name="responses")


class EventFormResponse(AbstractFormResponse):
    form = models.ForeignKey("forms.EventForm", on_delete=models.CASCADE, related_name="responses")
