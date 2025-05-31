from __future__ import annotations

import logging
from collections.abc import Iterable
from functools import cached_property
from typing import Any

import pydantic
from django.db import models

from core.utils.model_utils import make_slug_field
from dimensions.filters import DimensionFilters
from dimensions.models.scope import Scope
from dimensions.models.universe import Universe
from dimensions.utils.dimension_cache import DimensionCache
from graphql_api.language import DEFAULT_LANGUAGE

from .enums import SurveyApp
from .response import Response
from .splat import Splat
from .survey import Survey

logger = logging.getLogger("kompassi")


class ProjectionValidated(pydantic.BaseModel):
    """
    Projection has a bunch of JSONFields we want to validate and use in a type-safe way.
    """

    splats: list[Splat] = pydantic.Field(default_factory=list)
    required_dimensions: dict[str, list[str]] = pydantic.Field(default_factory=dict)
    projected_dimensions: dict[str, str] = pydantic.Field(default_factory=dict)
    filterable_dimensions: list[str] = pydantic.Field(default_factory=list)
    order_by: list[str] = pydantic.Field(default_factory=list)

    @pydantic.field_validator("splats", mode="after")
    def validate_splats(cls, splats: list[Splat]) -> list[Splat]:
        if not splats:
            return splats

        # All splats must have an equal number of source fields.
        source_fields_count = len(splats[0].source_fields)

        for splat in splats:
            if len(splat.source_fields) != source_fields_count:
                raise ValueError(
                    "All splats must have the same number of source fields. "
                    f"Expected {source_fields_count}, got {len(splat.source_fields)}."
                )

        return splats


class Projection(models.Model):
    """
    A Projection can be used to produce ad-hoc APIs from survey responses.
    """

    scope: models.ForeignKey[Scope] = models.ForeignKey(
        Scope,
        on_delete=models.CASCADE,
        related_name="projections",
    )

    is_public = models.BooleanField(
        default=False,
        help_text="if False, the projection API will require CBAC authorization",
    )

    default_language_code = models.CharField(
        max_length=2,
        default=DEFAULT_LANGUAGE,
    )

    slug = make_slug_field(unique=False)

    surveys = models.ManyToManyField(
        Survey,
        related_name="projections",
        blank=True,
        help_text="These surveys must share a Universe.",
    )

    splats = models.JSONField(
        default=list,
        blank=True,
    )

    required_dimensions = models.JSONField(
        default=dict,
        blank=True,
        help_text="dimension slug -> list of dimension value slugs",
    )

    projected_dimensions = models.JSONField(
        default=dict,
        blank=True,
        help_text="target field name -> dimension slug",
    )

    filterable_dimensions = models.JSONField(
        default=list,
        blank=True,
        help_text="List of dimension slugs that can be used to filter the projection results.",
    )

    order_by = models.JSONField(
        default=list,
        blank=True,
        help_text="List of resulting (projected) field names to order the projection results by.",
    )

    class Meta:
        unique_together = (("scope", "slug"),)

    def __str__(self) -> str:
        return f"{self.scope}/{self.slug}"

    @cached_property
    def app(self) -> SurveyApp:
        surveys = list(self.surveys.all())
        if not surveys:
            raise ValueError("Projection must have at least one survey to determine the app.")

        app = SurveyApp(surveys.pop(0).app)

        if any(SurveyApp(survey.app) != app for survey in surveys):
            raise ValueError("All surveys in a projection must share the same app.")

        return app

    @cached_property
    def universe(self) -> Universe:
        surveys = list(self.surveys.all())
        if not surveys:
            raise ValueError("Projection must have at least one survey to determine the universe.")

        universe = surveys.pop(0).universe

        if any(survey.universe != universe for survey in surveys):
            raise ValueError("All surveys in a projection must share the same universe.")

        return universe

    @cached_property
    def validated_fields(self) -> ProjectionValidated:
        return ProjectionValidated.model_validate(
            self,
            from_attributes=True,
        )

    def filter_responses(
        self,
        user_filters: DimensionFilters | None = None,
    ) -> models.QuerySet[Response]:
        dimension_filters = DimensionFilters()
        validated = self.validated_fields

        # could also raise 400 if trying to filter on a dimension that is not filterable?
        if user_filters is not None:
            for dimension_slug in validated.filterable_dimensions:
                if dimension_slug in user_filters.filters:
                    dimension_filters.filters[dimension_slug] = user_filters.filters[dimension_slug]

        dimension_filters.filters.update(validated.required_dimensions)

        return dimension_filters.filter(
            Response.objects.filter(
                form__survey__in=self.surveys.all(),
                superseded_by__isnull=True,
            ).select_related(
                "form",
                "form__survey",
            )
        )

    @staticmethod
    def get_formatted_field_name(field_name: str) -> str:
        """
        >>> Projection.get_formatted_field_name("exampleField")
        'formattedExampleField'
        """
        return "formatted" + field_name[0].upper() + field_name[1:]

    def sort_key(self, item: dict[str, Any]) -> tuple:
        """
        Returns a sort key for the given item based on the order_by field names.
        """
        return tuple(item.get(field_name, "") for field_name in self.validated_fields.order_by)

    def project(
        self,
        user_filters: DimensionFilters | None = None,
        lang: str | None = None,
    ) -> list[dict[str, Any]]:
        result = list(
            self._project(
                responses=self.filter_responses(user_filters=user_filters),
                lang=self.default_language_code if lang is None else lang,
                cache=self.universe.preload_dimensions(),
            )
        )

        if self.validated_fields.order_by:
            result.sort(key=self.sort_key)

        return result

    def _project(
        self,
        responses: Iterable[Response],
        *,
        lang: str,
        cache: DimensionCache,
    ) -> Iterable[dict[str, Any]]:
        for response in responses:
            yield from self._project_response(
                response,
                lang=lang,
                cache=cache,
            )

    def _project_response(
        self,
        response: Response,
        *,
        lang: str,
        cache: DimensionCache,
    ) -> Iterable[dict[str, Any]]:
        validated = self.validated_fields
        values, warnings = response.get_processed_form_data(
            field_slugs=[source_field for splat in validated.splats for source_field in splat.source_fields]
        )

        item_dimensions: dict[str, Any] = {}
        for target_field_name, dimension_slug in validated.projected_dimensions.items():
            formatted_field_name = self.get_formatted_field_name(target_field_name)
            dimension = cache.dimensions[dimension_slug]
            dimension_values = response.cached_dimensions.get(dimension_slug, [])

            if dimension.is_multi_value:
                item_dimensions[target_field_name] = dimension_values
            else:
                if not dimension_values:
                    item_dimensions[target_field_name] = ""
                    item_dimensions[formatted_field_name] = ""
                    continue
                elif len(dimension_values) > 1:
                    logger.warning(
                        "Single-value dimension has multiple values (projecting only the first one): %s",
                        dict(
                            projection=str(self),
                            survey=str(response.survey),
                            response_id=response.id,
                            target_field=target_field_name,
                            dimension_slug=dimension_slug,
                            dimension_values=dimension_values,
                        ),
                    )

                item_dimensions[target_field_name] = dimension_values[0]

            formatted_dimension_values = ", ".join(
                cache.values_by_dimension[dimension_slug][value_slug].get_title(lang) for value_slug in dimension_values
            )
            item_dimensions[formatted_field_name] = formatted_dimension_values

        for splat in validated.splats:
            for source_field in splat.source_fields:
                if source_field in values and (field_warnings := warnings.get(source_field, [])):
                    logger.warning(
                        "Cowardly refusing to project a value that has warnings: %s",
                        dict(
                            projection=str(self),
                            survey=str(response.survey),
                            response_id=response.id,
                            target_field=splat.target_field,
                            source_field=source_field,
                            field_warnings=field_warnings,
                        ),
                    )
                    del values[source_field]

        for item in Splat.project(validated.splats, values):
            yield dict(
                **item,
                **item_dimensions,
            )
