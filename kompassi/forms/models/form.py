from __future__ import annotations

import logging
from collections.abc import Iterable
from functools import cached_property
from typing import TYPE_CHECKING, Any, Self

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.http import HttpRequest

from kompassi.access.cbac import is_graphql_allowed_for_model
from kompassi.core.models.event import Event
from kompassi.graphql_api.language import DEFAULT_LANGUAGE, get_language_choices

from .field import Field
from .survey import Survey

if TYPE_CHECKING:
    from .response import Response


logger = logging.getLogger(__name__)


class Form(models.Model):
    """
    A Form is a language version of a Survey. (TODO rename?)
    A Form cannot exist without a Survey.
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="forms")
    survey: models.ForeignKey[Survey] = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name="languages",
    )
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
    id: int
    all_responses: models.QuerySet[Response]

    class Meta:
        unique_together = [("event", "survey", "language")]

    def __str__(self):
        return f"{self.event.slug if self.event else None}/{self.survey.slug}-{self.language}"

    def save(self, *, update_fields: Iterable[str] | None = None, **kwargs):
        if update_fields is None:
            self.with_cached_fields()
        else:
            update_fields = set(update_fields)
            if "fields" in update_fields:
                self.with_cached_fields()
                update_fields.add("cached_enriched_fields")

        super().save(update_fields=update_fields, **kwargs)

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
            and not self.all_responses.exists()
        )

    @classmethod
    def refresh_cached_fields_qs(cls, qs: models.QuerySet[Self], batch_size: int = 100):
        cls.objects.bulk_update(
            [form.with_cached_fields() for form in qs], ["cached_enriched_fields"], batch_size=batch_size
        )

    def with_cached_fields(self):
        self.cached_enriched_fields = [self._enrich_field(field) for field in self.fields]
        return self

    def refresh_cached_fields(self):
        self.with_cached_fields().save(update_fields=["cached_enriched_fields"])

    def _enrich_field(self, field: dict[str, Any]) -> dict[str, Any]:
        """
        Some field types may contain server side directives that need to be resolved before
        turning the form specification over to the frontend.
        """

        # TODO(#643) subsetValues
        if field.get("type") in ("DimensionSingleSelect", "DimensionMultiSelect") and (
            dimension_slug := field.get("dimension")
        ):
            dimension = self.survey.universe.dimensions.get(slug=dimension_slug)
            field = dict(
                field,
                choices=[choice.model_dump(by_alias=True) for choice in dimension.as_choices(self.language)],
            )

        return field

    @cached_property
    def validated_fields(self) -> list[Field]:
        return [Field.model_validate(field_dict) for field_dict in self.cached_enriched_fields]

    @property
    def scope(self):
        return self.survey.scope

    def clone(self, survey: Survey, created_by: AbstractBaseUser | None = None):
        form = Form(
            event=survey.event,
            survey=survey,
            language=self.language,
            title=self.title,
            description=self.description,
            thank_you_message=self.thank_you_message,
            fields=self.fields,
            created_by=created_by,
        )
        form.save()
        return form

    def replace_field(self, field_slug: str, field: Field):
        """
        Replace a field in the form with a new field.

        :param field_slug: The slug of the field to replace. Separate from field to allow replacing a field with one that has a different slug.
        :param field: The new field to replace the old one with.
        :raises KeyError: If the field with the given slug is not found in the form.

        NOTE: You are responsible for calling .save(["fields", "cached_enriched_fields"]) after this.
        """
        for i, f in enumerate(self.validated_fields):
            if f.slug == field_slug:
                self.fields[i] = field.model_dump(mode="json", by_alias=True, exclude_unset=True, exclude_none=True)
                break
        else:
            raise KeyError(f"Field {field.slug} not found in form {self}")

        del self.validated_fields
