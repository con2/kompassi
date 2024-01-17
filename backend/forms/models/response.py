from __future__ import annotations

import uuid
from functools import cached_property
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from ..utils.process_form_data import FieldWarning
    from .field import Field


class Response(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey("forms.Form", on_delete=models.CASCADE, related_name="responses")
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

    def get_processed_form_data(self, fields: list[Field]):
        """
        While one would normally use `values`, that needs access to the form.
        If processing multiple responses, it is more efficient to use this method
        as it avoids a round-trip to the database for each response.
        """
        from ..utils.process_form_data import process_form_data

        return process_form_data(fields, self.form_data)

    @cached_property
    def processed_form_data(self):
        from ..utils.process_form_data import process_form_data

        return process_form_data(self.form.validated_fields, self.form_data)

    @property
    def values(self) -> dict[str, Any]:
        return self.processed_form_data[0]

    @property
    def warnings(self) -> dict[str, list[FieldWarning]]:
        return self.processed_form_data[1]
