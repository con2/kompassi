from __future__ import annotations

import logging
import uuid
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.db import models, transaction
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

from .form import Form

if TYPE_CHECKING:
    from ..utils.process_form_data import FieldWarning
    from .dimension import Dimension, DimensionValue, ResponseDimensionValue
    from .field import Field
    from .survey import Survey


logger = logging.getLogger("kompassi")


class Response(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="responses")
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

    def _build_cached_dimensions(self) -> dict[str, list[str]]:
        """
        Used by ..handlers/dimension.py to populate cached_dimensions
        """
        new_cached_dimensions = {}
        for sdv in self.dimensions.all():
            new_cached_dimensions.setdefault(sdv.dimension.slug, []).append(sdv.value.slug)

        return new_cached_dimensions

    @classmethod
    @transaction.atomic
    def refresh_cached_dimensions_qs(cls, responses: models.QuerySet[Response]):
        bulk_update = []
        for response in (
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
            response.cached_dimensions = response._build_cached_dimensions()
            bulk_update.append(response)
        cls.objects.bulk_update(bulk_update, ["cached_dimensions"])

    def refresh_cached_dimensions(self):
        self.cached_dimensions = self._build_cached_dimensions()
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
        bulk_create: list[ResponseDimensionValue] = []

        # only these fields have the potential of being dimension fields
        # TODO support single checkbox as dimension field?
        # TODO use pydantic versions of fields? Must not be enriched (it removes choicesFrom)
        fields = [
            field
            for field in self.form.fields
            if field["slug"] in dimensions_by_slug
            and field["type"] in ("SingleSelect", "MultiSelect")
            and field["choicesFrom"] == {"dimension": field["slug"]}
        ]
        fields_by_slug = {field["slug"]: field for field in fields}

        # get_processed_form_data expects enriched, validated form of fields
        enriched_fields = [field for field in self.form.validated_fields if field.slug in fields_by_slug]
        values, warnings = self.get_processed_form_data(enriched_fields)

        # we have all the dimensions and values preloaded, so it makes sense to build cached_dimensions here
        cached_dimensions = {}

        def set_dimension_value(dimension: Dimension, value: DimensionValue):
            bulk_create.append(
                ResponseDimensionValue(
                    response=self,
                    dimension=dimension,
                    value=value,
                )
            )
            cached_dimensions.setdefault(dimension.slug, []).append(value.slug)

        for dimension in dimensions_by_slug.values():
            values_by_slug = values_by_dimension_by_slug[dimension.slug]

            # set initial values
            for value in values_by_slug.values():
                if value.is_initial:
                    set_dimension_value(dimension, value)

            dimension_field = fields_by_slug.get(dimension.slug)
            if not dimension_field:
                # this dimension is not present as a field on the form
                continue

            if field_warnings := warnings.get(dimension.slug):
                # this dimension has validation warnings
                logger.warning(
                    f"Response {self.id}: Refusing to lift {dimension.slug} "
                    f"that has validation warnings: {field_warnings}"
                )
                continue

            value_slugs: list[str]
            match dimension_field.get("type", "SingleSelect"):
                case "MultiSelect":
                    value_slugs = values.get(dimension.slug, [])
                case "SingleSelect":
                    value_slugs = [value_slug] if (value_slug := values.get(dimension.slug)) else []
                case _:
                    logger.warning(
                        f"Response {self.id}: Unexpected field type {dimension_field['type']} "
                        f"for dimension {dimension.slug}"
                    )
                    continue

            if not isinstance(value_slugs, list):
                logger.warning(f"Response {self.id}: Expected list of slugs for dimension field {dimension.slug}")
                continue

            for value_slug in value_slugs:
                value = values_by_slug.get(value_slug)
                if value is None:
                    logger.warning(f"Response {self.id}: Invalid value {value_slug} for dimension {dimension.slug}")
                    continue

                set_dimension_value(dimension, value)

        # NOTE: if we allow dimensions having initial values to be presented as fields on the form,
        # need to add ignore_conflicts=True here or rethink this somehow
        ResponseDimensionValue.objects.bulk_create(bulk_create)

        # mass delete and bulk create don't trigger signals (which is good)
        self.cached_dimensions = cached_dimensions
        self.save(update_fields=["cached_dimensions"])

    @transaction.atomic
    def set_dimension_values(self, values_to_set: dict[str, list[str]]):
        """
        Changes only those dimension values that are present in dimension_values.
        """
        from .dimension import ResponseDimensionValue

        survey = self.survey
        if survey is None:
            raise ValueError("Cannot set dimension values for a response that is not related to a survey")

        dimensions_by_slug, values_by_dimension_by_slug = survey.preload_dimensions(values_to_set)

        cached_dimensions = self.cached_dimensions
        bulk_delete = self.dimensions.filter(dimension__slug__in=dimensions_by_slug.keys())
        bulk_create: list[ResponseDimensionValue] = []

        for dimension_slug, value_slugs in values_to_set.items():
            bulk_delete = bulk_delete.exclude(dimension__slug=dimension_slug, value__slug__in=value_slugs)

            dimension = dimensions_by_slug[dimension_slug]
            values_by_slug = values_by_dimension_by_slug[dimension_slug]

            for value_slug in value_slugs:
                if value_slug not in cached_dimensions.get(dimension_slug, []):
                    value = values_by_slug[value_slug]
                    bulk_create.append(
                        ResponseDimensionValue(
                            response=self,
                            dimension=dimension,
                            value=value,
                        )
                    )

        bulk_delete.delete()
        ResponseDimensionValue.objects.bulk_create(bulk_create)

        # mass delete and bulk create don't trigger signals (which is good)
        self.cached_dimensions = dict(self.cached_dimensions, **values_to_set)
        self.save(update_fields=["cached_dimensions"])

    def get_processed_form_data(
        self,
        fields: Sequence[Field] | None = None,
    ) -> tuple[dict[str, Any], dict[str, list[FieldWarning]]]:
        """
        If you only need a subset of fields, pass them in as fields.
        Returns a tuple of (values, warnings).
        """
        from ..utils.process_form_data import process_form_data

        if fields is None:
            fields = self.form.validated_fields

        return process_form_data(fields, self.form_data)
