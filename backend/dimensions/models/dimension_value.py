from __future__ import annotations

import logging

from django.db import models
from django.http import HttpRequest

from access.cbac import is_graphql_allowed_for_model
from core.utils.model_utils import make_slug_field
from graphql_api.language import DEFAULT_LANGUAGE, getattr_message_in_language

from .dimension import Dimension
from .scope import Scope
from .universe import Universe

logger = logging.getLogger("kompassi")


class DimensionValue(models.Model):
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name="values")

    is_technical = models.BooleanField(
        default=False,
        help_text="Technical values cannot be edited in the UI. They are used for internal purposes and have some assumptions about them.",
    )

    is_subject_locked = models.BooleanField(
        default=False,
        help_text="If set, subjects this value is assigned to can no longer be edited by whomever submitted them.",
    )

    order = models.SmallIntegerField(
        default=0,
        help_text="Only applies if `dimension.value_ordering` is `manual`.",
    )

    slug = make_slug_field(unique=False, separator="-")
    color = models.CharField(max_length=63, blank=True, default="")

    # NOTE SUPPORTED_LANGUAGES
    title_en = models.TextField(blank=True, default="")
    title_fi = models.TextField(blank=True, default="")
    title_sv = models.TextField(blank=True, default="")

    @property
    def title_dict(self) -> dict[str, str]:
        """
        Returns a dictionary of titles in all supported languages.
        """
        return {
            # NOTE SUPPORTED_LANGUAGES
            "en": self.title_en,
            "fi": self.title_fi,
            "sv": self.title_sv,
        }

    def get_title(self, lang: str = DEFAULT_LANGUAGE) -> str:
        return getattr_message_in_language(self, "title", lang)

    def __str__(self):
        return self.slug

    @property
    def universe(self) -> Universe:
        return self.dimension.universe

    @property
    def scope(self) -> Scope:
        return self.dimension.scope

    @property
    def is_in_use(self) -> bool:
        from forms.models.response_dimension_value import ResponseDimensionValue
        from program_v2.models.program_dimension_value import ProgramDimensionValue

        match self.universe.app:
            case "forms":
                return ResponseDimensionValue.objects.filter(value=self).exists()
            case "program_v2":
                return ProgramDimensionValue.objects.filter(value=self).exists()
            case _:
                raise NotImplementedError(self.universe.app)

    def can_be_deleted_by(self, request: HttpRequest) -> bool:
        return (
            is_graphql_allowed_for_model(
                request.user,
                instance=self,
                operation="delete",
                field="self",
                app=self.universe.app,
            )
            and not self.is_technical
            and not self.is_in_use
        )

    class Meta:
        # the ordering will often be overridden by Dimension.value_ordering
        ordering = ("dimension", "order", "slug")
        unique_together = ("dimension", "slug")


# NOTE: ResponseDimensionValue provided by the forms app, ProgramDimensionValue provided by the program_v2 app
