from __future__ import annotations

import logging

from django.db import models

from core.utils.model_utils import make_slug_field

from .dimension import Dimension
from .scope import Scope
from .universe import Universe

logger = logging.getLogger("kompassi")


class DimensionValue(models.Model):
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name="values")

    # Note that if we define a concept of default values, they should be pre-selected on forms and overridable by user.
    # Contrast this to initial values that are instead set always and cannot be overridden by user.
    # An initial value should probably not be set on a dimension that is presented as a form field.
    is_initial = models.BooleanField(
        default=False,
        help_text="Initial values are set on new atoms automatically.",
    )

    order = models.SmallIntegerField(
        default=0,
        help_text="Only applies if `dimension.value_ordering` is `manual`.",
    )

    slug = make_slug_field(unique=False, separator="_")
    color = models.CharField(max_length=63, blank=True, default="")

    # NOTE SUPPORTED_LANGUAGES
    title_en = models.TextField(blank=True, default="")
    title_fi = models.TextField(blank=True, default="")
    title_sv = models.TextField(blank=True, default="")

    def __str__(self):
        return self.slug

    @property
    def universe(self) -> Universe:
        return self.dimension.universe

    @property
    def scope(self) -> Scope:
        return self.dimension.scope

    @property
    def can_remove(self) -> bool:
        from forms.models.response_dimension_value import ResponseDimensionValue
        from program_v2.models.dimension_values import ProgramDimensionValue

        match self.universe.app:
            case "forms":
                return not ResponseDimensionValue.objects.filter(value=self).exists()
            case "program_v2":
                return not ProgramDimensionValue.objects.filter(value=self).exists()
            case _:
                raise NotImplementedError(self.universe.app)

    class Meta:
        # the ordering will often be overridden by Dimension.value_ordering
        ordering = ("dimension", "order", "slug")
        unique_together = ("dimension", "slug")


# NOTE: ResponseDimensionValue provided by the forms app, ProgramDimensionValue provided by the program_v2 app
