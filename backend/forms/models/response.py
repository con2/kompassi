from __future__ import annotations

import uuid
from collections.abc import Collection, Mapping
from functools import cached_property
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from ..utils.process_form_data import FieldWarning
    from .dimension import ResponseDimensionValue
    from .field import Field
    from .survey import Survey


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

    # denormalized fields
    cached_dimensions = models.JSONField(
        default=dict,
        help_text="dimension slug -> list of value slugs",
    )

    # related fields
    dimensions: models.QuerySet[ResponseDimensionValue]

    @property
    def survey(self) -> Survey | None:
        return self.form.survey

    def build_cached_dimensions(self) -> dict[str, list[str]]:
        """
        Used by ..handlers/dimension.py to populate cached_dimensions
        """
        # TODO should all survey dimensions always be present, or only those with values?
        # TODO when dimensions are changed for an survey, refresh all cached_dimensions
        survey = self.survey
        if survey is None:
            return {}

        dimensions = {dimension.slug: [] for dimension in survey.dimensions.all()}
        for sdv in self.dimensions.all():
            dimensions[sdv.dimension.slug].append(sdv.value.slug)
        return dimensions

    @classmethod
    def refresh_cached_dimensions(cls, responses: models.QuerySet[Response]):
        for program in (
            responses.select_for_update(of=("self",))
            .only("id", "cached_dimensions")
            .prefetch_related(
                "dimensions__dimension__slug",
                "dimensions__value__slug",
            )
        ):
            program.cached_dimensions = program.build_cached_dimensions()
            program.save(update_fields=["cached_dimensions"])

    def lift_dimension_values(self):
        """
        Lifts the values of dimensions from form data into proper dimension values.
        This makes sense only for responses that are related to a survey.
        """
        survey = self.survey
        assert survey is not None, "Cannot lift dimension values for a response that is not related to a survey"

        for dimension in survey.dimensions.all():
            # set initial values
            for initial_value in dimension.values.filter(is_initial=True):
                self.dimensions.create(dimension=dimension, value=initial_value)

            # TODO cache a dict of slug -> field?
            # TODO use pydantic versions of fields? Must not be enriched (it removes choicesFrom)
            dimension_field = next(
                (
                    field
                    for field in self.form.fields
                    # TODO is it reasonable to require field["slug"] == dimension.slug?
                    if field["slug"] == dimension.slug and field.get("choicesFrom") == {"dimension": dimension.slug}
                ),
                None,
            )
            if not dimension_field:
                # this dimension is not present as a field on the form
                continue

            value_slug = self.values.get(dimension.slug)
            if not value_slug:
                # this dimension is not present in the response
                continue

            value = dimension.values.filter(slug=value_slug).first()
            if value is None:
                # invalid value for dimension
                continue

            # get_or_create to avoid collision with initial values
            # (probably shouldn't put a dimension that has an initial value on a form as a field?)
            self.dimensions.get_or_create(dimension=dimension, value=value)

    def set_dimension_values(self, dimension_values: Mapping[str, Collection[str]]):
        assert self.survey

        for dimension_slug, value_slugs in dimension_values.items():
            dimension = self.survey.dimensions.get(slug=dimension_slug)

            # remove values that should no longer be present
            self.dimensions.filter(dimension=dimension).exclude(value__slug__in=value_slugs).delete()

            for value_slug in value_slugs:
                value = dimension.values.get(slug=value_slug)
                self.dimensions.get_or_create(dimension=dimension, value=value)

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
