import logging
from copy import deepcopy
from functools import cached_property
from typing import Any

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import SLUG_FIELD_PARAMS, NONUNIQUE_SLUG_FIELD_PARAMS
from program_v2.models.dimension import Dimension


logger = logging.getLogger("kompassi")

LAYOUT_CHOICES = [
    ("horizontal", _("Horizontal")),
    ("vertical", _("Vertical")),
]

DEFAULT_LANGUAGE: str = settings.LANGUAGE_CODE


class AbstractForm(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
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
            assert len(choices_from) == 1, "choicesFrom must have exactly one key: value pair"
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
