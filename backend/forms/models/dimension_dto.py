from __future__ import annotations

import logging
from typing import Self

import pydantic

from dimensions.models.dimension import Dimension
from dimensions.models.dimension_value import DimensionValue
from graphql_api.language import SUPPORTED_LANGUAGES

from ..utils.process_form_data import process_form_data
from .field import Field, FieldType
from .survey import Survey

logger = logging.getLogger("kompassi")


def unpack_localized_value(form_data: dict[str, str], field_name: str) -> dict[str, str | dict[str, str]]:
    """
    In some forms, localized values are splat into multiple fields title.fi, title.en etc.
    Database expects them as a single JSON field. Do the needful.
    """
    prefix = f"{field_name}."
    title = {key.removeprefix(prefix): value for key, value in form_data.items() if key.startswith(prefix)}
    data: dict[str, str | dict[str, str]] = {
        key: value for key, value in form_data.items() if not key.startswith(prefix)
    }
    data["title"] = title
    return data


class DimensionValueDTO(pydantic.BaseModel, populate_by_name=True):
    slug: str
    title: dict[str, str]
    color: str = ""
    is_initial: bool = pydantic.Field(default=False, alias="isInitial")

    @classmethod
    def from_model(cls, value: DimensionValue) -> Self:
        return cls(
            slug=value.slug,
            title={
                lang.code: title_in_lang
                for lang in SUPPORTED_LANGUAGES
                if (title_in_lang := getattr(value, f"title_{lang.code}", ""))
            },  # type: ignore
            color=value.color,
            isInitial=value.is_initial,
        )

    def save(self, dimension: Dimension):
        DimensionValue.objects.update_or_create(
            dimension=dimension,
            slug=self.slug,
            defaults=dict(
                # NOTE SUPPORTED_LANGUAGES
                title_en=self.title.get("en", ""),
                title_fi=self.title.get("fi", ""),
                title_sv=self.title.get("sv", ""),
                color=self.color,
                is_initial=self.is_initial,
            ),
        )

    @classmethod
    def from_form_data(cls, form_data: dict[str, str]) -> Self:
        """
        Used by dimension editor to create and edit dimension values.
        The localized title field is presented as field per language.
        """
        data = unpack_localized_value(form_data, "title")

        # FIXME the whole form needs to go through process_form_data but the form definition is generated clientside
        fields = [Field(slug="isInitial", type=FieldType.SINGLE_CHECKBOX)]
        data2, _warnings = process_form_data(fields, form_data)
        data = dict(data, **data2)

        print(data)

        return cls.model_validate(data)


class DimensionDTO(pydantic.BaseModel, populate_by_name=True):
    """
    Helper to load dimensions from YAML, form data or similar external sources.
    """

    slug: str = pydantic.Field(min_length=1)
    title: dict[str, str]
    choices: list[DimensionValueDTO] | None = pydantic.Field(default=None)
    is_key_dimension: bool = pydantic.Field(default=False, alias="isKeyDimension")
    is_multi_value: bool = pydantic.Field(default=False, alias="isMultiValue")
    is_shown_to_subject: bool = pydantic.Field(default=False, alias="isShownToSubject")

    @classmethod
    def from_model(cls, dimension: Dimension) -> Self:
        return cls(
            slug=dimension.slug,
            title={
                lang.code: title_in_lang
                for lang in SUPPORTED_LANGUAGES
                if (title_in_lang := getattr(dimension, f"title_{lang.code}", ""))
            },  # type: ignore
            isKeyDimension=dimension.is_key_dimension,
            isMultiValue=dimension.is_multi_value,
            isShownToSubject=dimension.is_shown_to_subject,
            choices=[DimensionValueDTO.from_model(value) for value in dimension.values.all()],
        )

    def save(self, survey: Survey, order: int = 0):
        dimension, created = Dimension.objects.update_or_create(
            universe=survey.universe,
            slug=self.slug,
            defaults=dict(
                # NOTE SUPPORTED_LANGUAGES
                title_en=self.title.get("en", ""),
                title_fi=self.title.get("fi", ""),
                title_sv=self.title.get("sv", ""),
                is_key_dimension=self.is_key_dimension,
                is_multi_value=self.is_multi_value,
                is_shown_to_subject=self.is_shown_to_subject,
                order=order,
            ),
        )

        if self.choices is None:
            return dimension

        # delete choices that are no longer present
        if not created:
            DimensionValue.objects.filter(dimension=dimension).exclude(
                slug__in=[choice.slug for choice in self.choices]
            ).delete()

        for choice in self.choices:
            choice.save(dimension)

        return dimension

    @classmethod
    def save_many(cls, survey: Survey, dimensions: list[Self]):
        # TODO(perf) bulk save & refresh once
        order = 0
        for dimension in dimensions:
            order += 10
            dimension.save(survey, order)

    @classmethod
    def from_form_data(cls, form_data: dict[str, str]) -> Self:
        """
        Used by dimension editor to create and edit dimensions.
        The localized title field is presented as field per language.
        """
        data = unpack_localized_value(form_data, "title")

        return cls.model_validate(data)
