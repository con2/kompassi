from __future__ import annotations

import logging
from copy import deepcopy
from functools import cached_property
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS
from program_v2.models.dimension import Dimension

from .field import Field

if TYPE_CHECKING:
    from .response import Response
    from .survey import Survey


logger = logging.getLogger("kompassi")

LAYOUT_CHOICES = [
    ("horizontal", _("Horizontal")),
    ("vertical", _("Vertical")),
]

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


class Form(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="forms")
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    thank_you_message = models.TextField(blank=True, default="")
    language = models.CharField(max_length=2, default=DEFAULT_LANGUAGE, choices=settings.LANGUAGES)
    layout = models.CharField(
        verbose_name=_("Layout"),
        choices=LAYOUT_CHOICES,
        max_length=max(len(c) for (c, t) in LAYOUT_CHOICES),
        default=LAYOUT_CHOICES[0][0],
    )

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fields = models.JSONField()

    responses: models.QuerySet[Response]

    class Meta:
        unique_together = [("event", "slug")]

    def __str__(self):
        return self.title

    @cached_property
    def enriched_fields(self):
        return [self._enrich_field(field) for field in self.fields]

    def _enrich_field(self, field: dict[str, Any]) -> dict[str, Any]:
        """
        Some field types may contain server side directives that need to be resolved before
        turning the form specification over to the frontend.
        """
        field = deepcopy(field)

        if choices_from := field.get("choicesFrom"):
            if len(choices_from) != 1:
                raise AssertionError("choicesFrom must have exactly one key: value pair")
            ((source_type, source),) = choices_from.items()
            if source_type == "dimension":
                dimension = Dimension.objects.get(event=self.event, slug=source)
                field["choices"] = [
                    dict(
                        slug=value.slug,
                        title=value.title.translate(self.language),
                    )
                    for value in dimension.values.all()
                ]
            else:
                raise NotImplementedError(f"choicesFrom: {choices_from}")

            del field["choicesFrom"]

        return field

    @cached_property
    def validated_fields(self):
        return [Field.model_validate(field_dict) for field_dict in self.enriched_fields]

    @property
    def survey(self) -> Survey | None:
        from .survey import Survey

        # there can only be one
        try:
            return self.event.surveys.filter(languages=self).get()
        except Survey.DoesNotExist:
            return None
        except Survey.MultipleObjectsReturned:
            raise
