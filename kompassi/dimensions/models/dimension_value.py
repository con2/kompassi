from __future__ import annotations

import logging

from django.db import models

from kompassi.core.middleware import RequestWithCache
from kompassi.core.utils.model_utils import make_slug_field
from kompassi.graphql_api.language import DEFAULT_LANGUAGE, getattr_message_in_language

from .dimension import Dimension
from .scope import Scope
from .universe import Universe

logger = logging.getLogger(__name__)


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

    dimension_id: int
    id: int
    pk: int

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

    def can_be_deleted_by(self, request: RequestWithCache) -> bool:
        cache = request.kompassi_cache
        return (
            not self.is_technical
            and not cache.for_universe(self.universe).is_dimension_value_in_use(self)
            and cache.is_allowed(
                instance=self.dimension,
                operation="delete",
                field="values",
                app=self.universe.app_name,
            )
        )

    def can_be_updated_by(self, request: RequestWithCache) -> bool:
        cache = request.kompassi_cache
        return not self.is_technical and cache.is_allowed(
            instance=self.dimension,
            operation="update",
            field="values",
            app=self.universe.app_name,
        )

    class Meta:
        # the ordering will often be overridden by Dimension.value_ordering
        ordering = ("dimension", "order", "slug")
        unique_together = ("dimension", "slug")


# NOTE: ResponseDimensionValue provided by the forms app, ProgramDimensionValue provided by the program_v2 app
