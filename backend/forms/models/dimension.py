from __future__ import annotations

import logging
from typing import Self

import pydantic
from django.db import models

from core.models import Event
from core.utils.locale_utils import get_message_in_language
from core.utils.log_utils import log_get_or_create
from core.utils.model_utils import validate_slug

from ..utils.process_form_data import process_form_data
from .field import Choice, Field, FieldType
from .response import Response
from .survey import Survey

logger = logging.getLogger("kompassi")


class Dimension(models.Model):
    """
    Dimensions are "multiple choice fields on steroids" that can be used to
    implement filters, workflows and other use cases for survey responses.
    Dimensions may or may not be presented on the survey form.
    """

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="dimensions")
    slug = models.CharField(max_length=255, validators=[validate_slug])
    title = models.JSONField(blank=True, default=dict)
    order = models.IntegerField(default=0)
    is_key_dimension = models.BooleanField(
        default=False,
        help_text="Key dimensions are shown in the survey responses list.",
    )
    is_multi_value = models.BooleanField(
        default=False,
        help_text=(
            "Multi-value dimensions allow multiple values to be selected. "
            "NOTE: In the database, all dimensions are multi-value, so this is just a UI hint."
        ),
    )
    is_shown_to_respondent = models.BooleanField(
        default=False,
        help_text="If set, the respondent will see the value of the dimension in the profile survey responses list.",
    )

    values: models.QuerySet[DimensionValue]

    @property
    def event(self) -> Event:
        return self.survey.event

    @property
    def can_remove(self) -> bool:
        return not ResponseDimensionValue.objects.filter(dimension=self).exists()

    def get_choices(self, language: str | None = None) -> list[Choice]:
        return [
            Choice(
                slug=slug,
                title=get_message_in_language(title, language),  # type: ignore  # TODO why does this get typed as str and not dict?
            )
            for slug, title in self.values.all().values_list("slug", "title")
        ]

    def admin_get_event(self) -> Event:
        return self.event

    admin_get_event.short_description = "event"
    admin_get_event.admin_order_field = "survey__event"

    class Meta:
        unique_together = ("survey", "slug")
        ordering = ("survey", "order", "slug")

    def __str__(self):
        return self.slug


class DimensionValue(models.Model):
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name="values")
    slug = models.CharField(max_length=255, validators=[validate_slug])
    title = models.JSONField(blank=True, default=dict)
    color = models.CharField(max_length=63, blank=True, default="")

    # Note that if we define a concept of default values, they should be pre-selected on forms and overridable by user.
    # Contrast this to initial values that are instead set always and cannot be overridden by user.
    # An initial value should probably not be set on a dimension that is presented as a form field.
    is_initial = models.BooleanField(
        default=False,
        help_text="Initial values are set on new responses automatically.",
    )

    def __str__(self):
        return self.slug

    @property
    def event(self) -> Event:
        return self.dimension.event

    @property
    def survey(self) -> Survey:
        return self.dimension.survey

    @property
    def can_remove(self) -> bool:
        return not ResponseDimensionValue.objects.filter(value=self).exists()

    class Meta:
        unique_together = ("dimension", "slug")


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
            title=value.title,
            color=value.color,
            isInitial=value.is_initial,
        )

    def save(self, dimension: Dimension):
        DimensionValue.objects.update_or_create(
            dimension=dimension,
            slug=self.slug,
            defaults=dict(
                title=self.title,
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
    is_shown_to_respondent: bool = pydantic.Field(default=False, alias="isShownToRespondent")

    @classmethod
    def from_model(cls, dimension: Dimension) -> Self:
        return cls(
            slug=dimension.slug,
            title=dimension.title,
            isKeyDimension=dimension.is_key_dimension,
            isMultiValue=dimension.is_multi_value,
            isShownToRespondent=dimension.is_shown_to_respondent,
            choices=[DimensionValueDTO.from_model(value) for value in dimension.values.all()],
        )

    def save(self, survey: Survey, order: int = 0):
        dimension, created = Dimension.objects.update_or_create(
            survey=survey,
            slug=self.slug,
            defaults=dict(
                title=self.title,
                is_key_dimension=self.is_key_dimension,
                is_multi_value=self.is_multi_value,
                is_shown_to_respondent=self.is_shown_to_respondent,
                order=order,
            ),
        )

        log_get_or_create(logger, dimension, created)

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


class ResponseDimensionValue(models.Model):
    response = models.ForeignKey(
        Response,
        on_delete=models.CASCADE,
        related_name="dimensions",
    )
    dimension = models.ForeignKey(
        Dimension,
        on_delete=models.CASCADE,
        related_name="+",
    )
    value = models.ForeignKey(
        DimensionValue,
        on_delete=models.CASCADE,
        related_name="+",
    )

    def __str__(self):
        return f"{self.dimension}={self.value}"

    @property
    def event(self) -> Event:
        return self.dimension.event

    @property
    def survey(self) -> Survey:
        return self.dimension.survey

    class Meta:
        unique_together = ("response", "value")
