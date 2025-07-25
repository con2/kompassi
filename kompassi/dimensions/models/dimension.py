from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import get_language

from kompassi.core.middleware import RequestWithCache
from kompassi.core.utils.model_utils import make_slug_field
from kompassi.graphql_api.language import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGE_CODES, getattr_message_in_language

from .enums import ValueOrdering
from .scope import Scope
from .universe import Universe

if TYPE_CHECKING:
    from kompassi.forms.models.field import Choice

    from .dimension_value import DimensionValue


logger = logging.getLogger(__name__)


# Keep in sync with buildDimensionFilters in frontend/src/components/dimensions/helpers.ts
INVALID_DIMENSION_SLUGS = [
    # clash with field names in Program
    "slug",
    "title",
    "description",
    "annotations",
    # clash with query string parameters for ProgramFilters
    "favorited",
    "past",
    "display",
    "search",
    # Do or do not. There is no try.
    "error",
    "success",
    "force",
]


def invalid_slugs_validator(value: str) -> None:
    """
    Validator for dimension slugs. Raises a ValidationError if the slug is invalid.
    """
    if value in INVALID_DIMENSION_SLUGS:
        raise ValidationError(f"{value!r} is a reserved word that cannot be used as a dimension slug.")


class Dimension(models.Model):
    """
    Dimensions are "multiple choice fields on steroids" that can be used to
    implement filters, workflows and other use cases for survey responses.

    Dimension values may be attached to various things such as survey responses
    or program items. These things are called atoms.
    """

    universe: models.ForeignKey[Universe] = models.ForeignKey(
        Universe,
        on_delete=models.CASCADE,
        related_name="dimensions",
    )
    order = models.SmallIntegerField(default=0)

    is_public = models.BooleanField(
        default=True,
        help_text="Public dimensions are returned to non-admin users.",
    )
    is_key_dimension = models.BooleanField(
        default=False,
        help_text="Key dimensions are shown lists of atoms.",
    )
    is_multi_value = models.BooleanField(
        default=False,
        help_text=(
            "Multi-value dimensions allow multiple values to be selected. "
            "NOTE: In the database, all dimensions are multi-value, so this is just a UI hint."
        ),
    )
    is_list_filter = models.BooleanField(
        default=True,
        help_text="Suggests to UI that this dimension should be shown as a list filter.",
    )
    is_shown_in_detail = models.BooleanField(
        default=True,
        help_text="Suggests to UI that this dimension should be shown in detail view.",
    )
    is_negative_selection = models.BooleanField(
        default=False,
        help_text=(
            "Suggests to UI that when this dimension is not being filtered on, all values should be selected. "
            "Intended for use cases when the user is expected to rather exclude certain values than only include some. "
            "One such use case is accessibility and content warnings. "
            "NOTE: Does not make sense without `is_multi_value`."
        ),
    )

    is_technical = models.BooleanField(
        default=False,
        help_text=(
            "Technical dimensions are not editable in the UI. "
            "They are used for internal purposes have some assumptions about them (eg. their existence and that of certain values)."
        ),
    )
    can_values_be_added = models.BooleanField(
        default=True,
        help_text=(
            "If set, users can add values to this dimension in the UI and values added by the user can be edited. "
            "Some technical dimensions may allow adding values and some may not."
        ),
    )
    value_ordering = models.CharField(
        choices=ValueOrdering.choices,
        default=ValueOrdering.TITLE.value,
        max_length=max(len(value_ordering.value) for value_ordering in ValueOrdering),
        help_text=(
            "In which order are the values of this dimension returned in the GraphQL API. "
            "NOTE: When using Alphabetical (localized title), "
            "the language needs to be provided to `values` and `values.title` fields separately."
        ),
    )

    slug = make_slug_field(unique=False, separator="-", extra_validators=[invalid_slugs_validator])

    # NOTE SUPPORTED_LANGUAGES
    title_en = models.TextField(blank=True, default="")
    title_fi = models.TextField(blank=True, default="")
    title_sv = models.TextField(blank=True, default="")

    values: models.QuerySet[DimensionValue]
    id: int
    pk: int

    class Meta:
        ordering = ("universe", "order", "slug")
        constraints = [
            models.UniqueConstraint(
                fields=["universe", "slug"],
                name="dimension_unique_universe_slug",
            ),
        ]

    def __str__(self):
        return self.slug

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

    @property
    def scope(self) -> Scope:
        return self.universe.scope

    def get_value_order_field(self, language: str | None = None) -> str:
        if language not in SUPPORTED_LANGUAGE_CODES:
            language = get_language()

        match self.value_ordering:
            case ValueOrdering.TITLE:
                return f"title_{language}"
            case ValueOrdering.MANUAL:
                return "order"
            case ValueOrdering.SLUG:
                return "slug"
            case _:
                raise NotImplementedError(self.value_ordering)

    def get_values(self, language: str | None = None) -> models.QuerySet[DimensionValue]:
        """
        Use this method instead of self.values.all() when you want the values in the correct order.
        NOTE: If value_ordering is TITLE, you need to provide the language.
        """
        value_order_field = self.get_value_order_field(language)
        return self.values.all().order_by(value_order_field)

    def as_choices(self, language: str | None = None) -> list[Choice]:
        from kompassi.forms.models.field import Choice

        title_fields = [f"title_{lang}" for lang in SUPPORTED_LANGUAGE_CODES]

        # lift the selected language to the front
        if language in SUPPORTED_LANGUAGE_CODES:
            title_fields = [f"title_{language}"] + [field for field in title_fields if field != f"title_{language}"]

        return [
            Choice(
                slug=slug,
                title=next((localized_title for localized_title in localized_titles if localized_title), slug),
            )
            for slug, *localized_titles in self.get_values(language).values_list("slug", *title_fields)
        ]

    def get_title(self, lang: str = DEFAULT_LANGUAGE) -> str:
        return getattr_message_in_language(self, "title", lang)

    @admin.display(description="Title")
    def admin_get_title(self):
        return self.get_title(get_language())

    @admin.display(description="Scope", ordering="universe__scope__slug")
    def admin_get_scope(self):
        return self.universe.scope.slug if self.universe and self.universe.scope else None

    @admin.display(description="Universe", ordering="universe__slug")
    def admin_get_universe(self):
        return self.universe.slug if self.universe else None

    def can_be_deleted_by(self, request: RequestWithCache) -> bool:
        cache = request.kompassi_cache

        return (
            not self.is_technical
            and cache.is_allowed(
                instance=self,
                operation="delete",
                app=self.universe.app_name,
            )
            and not cache.for_universe(self.universe).is_dimension_in_use(self)
        )

    def can_values_be_created_by(self, request: RequestWithCache) -> bool:
        return self.can_values_be_added and request.kompassi_cache.is_allowed(
            instance=self,
            operation="create",
            app=self.universe.app_name,
            field="values",
        )

    def can_be_updated_by(self, request: RequestWithCache) -> bool:
        return request.kompassi_cache.is_allowed(
            instance=self,
            operation="update",
            app=self.universe.app_name,
        )

    def refresh_dependents(self):
        from kompassi.forms.models.form import Form

        Form.refresh_cached_fields_qs(Form.objects.filter(survey__universe=self.universe))
