from __future__ import annotations

import logging

import pydantic
from django.db import models

from core.models import Event
from core.utils.locale_utils import get_message_in_language
from core.utils.model_utils import validate_slug

from .field import Choice
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

    values: models.QuerySet[DimensionValue]

    @property
    def event(self) -> Event:
        return self.survey.event

    def get_choices(self, language: str | None = None) -> list[Choice]:
        return [
            Choice(
                slug=value.slug,
                title=get_message_in_language(value.title, language),  # type: ignore  # TODO why does this get typed as str and not dict?
            )
            for value in self.values.all()
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

    class Meta:
        unique_together = ("dimension", "slug")


class DimensionValueDTO(pydantic.BaseModel):
    slug: str
    title: dict[str, str]
    color: str = ""
    is_initial: bool = False

    def save(self, dimension: Dimension):
        # TODO change to get_or_create when form editor is implemented
        # so that these can be loaded once but user changes are not overwritten
        DimensionValue.objects.update_or_create(
            dimension=dimension,
            slug=self.slug,
            defaults=dict(
                title=self.title,
                color=self.color,
                is_initial=self.is_initial,
            ),
        )


class DimensionDTO(pydantic.BaseModel):
    """
    Helper to load dimensions from YAML.
    """

    slug: str
    title: dict[str, str]
    choices: list[DimensionValueDTO]
    order: int = 0
    is_key_dimension: bool = False

    def save(self, survey: Survey):
        # TODO change to get_or_create when form editor is implemented
        # so that these can be loaded once but user changes are not overwritten
        dimension, _created = Dimension.objects.update_or_create(
            survey=survey,
            slug=self.slug,
            defaults=dict(
                title=self.title,
                order=self.order,
                is_key_dimension=self.is_key_dimension,
            ),
        )

        # delete choices that are no longer present
        if not _created:
            DimensionValue.objects.filter(dimension=dimension).exclude(
                slug__in=[choice.slug for choice in self.choices]
            ).delete()

        for choice in self.choices:
            choice.save(dimension)


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
