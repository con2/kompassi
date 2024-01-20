from __future__ import annotations

import uuid
from collections.abc import Collection, Mapping
from functools import cached_property
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.db import models, transaction
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
        survey = self.survey
        if survey is None:
            return {}

        new_cached_dimensions = {}
        for sdv in self.dimensions.all():
            new_cached_dimensions.setdefault(sdv.dimension.slug, []).append(sdv.value.slug)

        return new_cached_dimensions

    @classmethod
    @transaction.atomic
    def refresh_cached_dimensions_qs(cls, responses: models.QuerySet[Response]):
        for survey in (
            responses.select_for_update(of=("self",))
            .prefetch_related(
                "dimensions__dimension",
                "dimensions__value",
            )
            .only(
                "id",
                "dimensions__dimension__slug",
                "dimensions__value__slug",
            )
        ):
            survey.refresh_cached_dimensions()

    def refresh_cached_dimensions(self):
        self.cached_dimensions = self.build_cached_dimensions()
        self.save(update_fields=["cached_dimensions"])

    @transaction.atomic
    def lift_dimension_values(self):
        """
        Lifts the values of dimensions from form data into proper dimension values.
        This makes sense only for responses that are related to a survey.

        NOTE: Expected to be called only right after creation.
        If you call this later, be sure to yeet the existing dimension values first,
        or rework this method to use set_dimension_values that accounts for existing ones.
        """
        from .dimension import ResponseDimensionValue

        survey = self.survey
        if survey is None:
            raise ValueError("Cannot lift dimension values for a response that is not related to a survey")

        dimensions_by_slug, values_by_dimension_by_slug = survey.preload_dimensions()
        rdvs_to_create: list[ResponseDimensionValue] = []
        fields_by_slug = {field["slug"]: field for field in self.form.fields}

        for dimension in dimensions_by_slug.values():
            values_by_slug = values_by_dimension_by_slug[dimension.slug]
            # set initial values
            rdvs_to_create.extend(
                ResponseDimensionValue(
                    response=self,
                    dimension=dimension,
                    value=value,
                )
                for value in values_by_slug.values()
                if value.is_initial
            )

            # TODO use pydantic versions of fields? Must not be enriched (it removes choicesFrom)
            dimension_field = fields_by_slug.get(dimension.slug)
            if not dimension_field:
                # this dimension is not present as a field on the form
                continue

            value_slug = self.values.get(dimension.slug)
            if not value_slug:
                # this dimension is not present in the response
                continue

            value = values_by_slug.get(value_slug)
            if value is None:
                # invalid value for dimension
                continue

            # get_or_create to avoid collision with initial values
            # (probably shouldn't put a dimension that has an initial value on a form as a field?)
            rdvs_to_create.append(
                ResponseDimensionValue(
                    response=self,
                    dimension=dimension,
                    value=value,
                )
            )

        # NOTE: if we allow dimensions having initial values to be presented as fields on the form,
        # need to add ignore_conflicts=True here or rethink this somehow
        ResponseDimensionValue.objects.bulk_create(rdvs_to_create)

        # mass delete and bulk create don't trigger signals (which is good)
        self.refresh_cached_dimensions()

    @transaction.atomic
    def set_dimension_values(
        self,
        dimension_values: Mapping[str, Collection[str]],
    ):
        from .dimension import ResponseDimensionValue

        survey = self.survey
        if survey is None:
            raise ValueError("Cannot set dimension values for a response that is not related to a survey")

        dimensions_by_slug, values_by_dimension_by_slug = survey.preload_dimensions(dimension_values)

        cached_dimensions = self.cached_dimensions
        qs_to_delete = self.dimensions.filter(dimension__slug__in=dimensions_by_slug.keys())
        rdvs_to_create: list[ResponseDimensionValue] = []

        for dimension_slug, value_slugs in dimension_values.items():
            qs_to_delete = qs_to_delete.exclude(dimension__slug=dimension_slug, value__slug__in=value_slugs)

            dimension = dimensions_by_slug[dimension_slug]
            values_by_slug = values_by_dimension_by_slug[dimension_slug]

            for value_slug in value_slugs:
                if value_slug not in cached_dimensions.get(dimension_slug, []):
                    value = values_by_slug[value_slug]
                    rdvs_to_create.append(
                        ResponseDimensionValue(
                            response=self,
                            dimension=dimension,
                            value=value,
                        )
                    )
        qs_to_delete.delete()
        ResponseDimensionValue.objects.bulk_create(rdvs_to_create)

        # mass delete and bulk create don't trigger signals (which is good)
        self.refresh_cached_dimensions()

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
