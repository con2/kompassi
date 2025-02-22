from __future__ import annotations

import logging
from copy import deepcopy
from functools import cached_property
from typing import TYPE_CHECKING, Any, Self

from django.conf import settings
from django.db import models, transaction
from django.http import HttpRequest

from access.cbac import is_graphql_allowed_for_model
from core.models.event import Event
from graphql_api.language import DEFAULT_LANGUAGE, get_language_choices

from .field import Field
from .survey import Survey

if TYPE_CHECKING:
    from .response import Response


logger = logging.getLogger("kompassi")


class Form(models.Model):
    """
    A Form is a language version of a Survey. (TODO rename?)
    A Form cannot exist without a Survey.
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="forms")
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="languages")
    language = models.CharField(
        max_length=2,
        default=DEFAULT_LANGUAGE,
        choices=get_language_choices(),
    )

    title = models.CharField(max_length=255, default="")
    description = models.TextField(blank=True, default="")
    thank_you_message = models.TextField(blank=True, default="")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fields = models.JSONField(default=list)

    # cached fields
    cached_enriched_fields = models.JSONField(default=list)

    # related fields
    responses: models.QuerySet[Response]

    class Meta:
        unique_together = [("event", "survey", "language")]

    def __str__(self):
        return f"{self.event.slug if self.event else None}/{self.survey.slug}-{self.language}"

    def can_be_deleted_by(self, request: HttpRequest):
        # TODO should we use Survey instead as a privileges root?
        return (
            is_graphql_allowed_for_model(
                request.user,
                instance=self,
                operation="delete",
                field="self",
                app=self.survey.app,
            )
            and not self.responses.exists()
        )

    @property
    def enriched_fields(self) -> list[dict[str, Any]]:
        """
        There is a chicken and egg problem with the enriched_fields property, mostly when
        Forms, Surveys and Dimensions are created programmatically (eg. in tests and setup scripts).
        If a `valueFrom` directive is used in a Field, the Form needs to belong to a Survey.
        """
        if not self.cached_enriched_fields:
            self.refresh_enriched_fields()

        return self.cached_enriched_fields

    @classmethod
    @transaction.atomic
    def refresh_enriched_fields_qs(cls, qs: models.QuerySet[Self]):
        """
        Refresh cached_enriched_fields for all forms in the queryset.
        """
        forms_to_update = []
        for form in qs.select_for_update(of=("self",)):
            form.cached_enriched_fields = form._build_enriched_fields()
            forms_to_update.append(form)
        cls.objects.bulk_update(forms_to_update, ["cached_enriched_fields"])

    def refresh_enriched_fields(self):
        """
        Refresh cached_enriched_fields for this form.
        NOTE: Use refresh_enriched_fields_qs for bulk updates.
        """
        self.cached_enriched_fields = self._build_enriched_fields()
        self.save(update_fields=["cached_enriched_fields"])

    def _build_enriched_fields(self) -> list[dict[str, Any]]:
        return [self._enrich_field(field) for field in self.fields]

    def _enrich_field(self, field: dict[str, Any]) -> dict[str, Any]:
        """
        Some field types may contain server side directives that need to be resolved before
        turning the form specification over to the frontend.
        """
        field = deepcopy(field)

        if choices_from := field.get("choicesFrom"):
            field["choices"] = []

            if len(choices_from) != 1:
                raise ValueError("choicesFrom must have exactly one key: value pair")

            # TODO(#554) type=DimensionSingleSelect, DimensionMultiSelect, DimensionMatrix instead of choicesFrom: dimension: foo
            ((source_type, source),) = choices_from.items()
            if source_type == "dimension":
                if survey := self.survey:
                    dimension = survey.universe.dimensions.get(slug=source)
                    field["choices"] = [
                        choice.model_dump(by_alias=True) for choice in dimension.as_choices(self.language)
                    ]
                else:
                    raise ValueError("A form that is not used as a survey or program offer form cannot use valuesFrom")

            else:
                raise NotImplementedError(f"choicesFrom: {choices_from}")

            del field["choicesFrom"]

        return field

    @cached_property
    def validated_fields(self) -> list[Field]:
        return [Field.model_validate(field_dict) for field_dict in self.enriched_fields]

    @property
    def scope(self):
        return self.survey.scope
