from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.contrib import admin
from django.db import models
from django.utils.translation import get_language

from core.utils.locale_utils import getattr_message_in_language
from core.utils.model_utils import make_slug_field
from graphql_api.language import SUPPORTED_LANGUAGE_CODES

from .scope import Scope
from .universe import Universe
from .value_ordering import ValueOrdering

if TYPE_CHECKING:
    from forms.models.field import Choice

    from .dimension_value import DimensionValue


logger = logging.getLogger("kompassi")


class Dimension(models.Model):
    """
    Dimensions are "multiple choice fields on steroids" that can be used to
    implement filters, workflows and other use cases for survey responses.

    Dimension values may be attached to various things such as survey responses
    or program items. These things are called atoms.
    """

    universe = models.ForeignKey(Universe, on_delete=models.CASCADE, related_name="dimensions")
    order = models.SmallIntegerField(default=0)

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
    is_shown_to_subject = models.BooleanField(
        default=False,
        help_text="If set, the subject will see the value of the dimension when atoms are listed in their profile.",
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

    slug = make_slug_field(unique=False, separator="_")

    # NOTE SUPPORTED_LANGUAGES
    title_en = models.TextField(blank=True, default="")
    title_fi = models.TextField(blank=True, default="")
    title_sv = models.TextField(blank=True, default="")

    values: models.QuerySet[DimensionValue]

    @property
    def scope(self) -> Scope:
        return self.universe.scope

    def get_value_order_field(self, language: str | None = None) -> str:
        if language not in SUPPORTED_LANGUAGE_CODES:
            language = get_language()

        if self.value_ordering == ValueOrdering.TITLE:
            return f"title_{language}"
        elif self.value_ordering == ValueOrdering.MANUAL:
            return "order"
        else:
            return "slug"

    def get_values(self, language: str | None = None):
        """
        Use this method instead of self.values.all() when you want the values in the correct order.
        NOTE: If value_ordering is TITLE, you need to provide the language.
        """
        value_order_field = self.get_value_order_field(language)
        return self.values.all().order_by(value_order_field)

    def as_choices(self, language: str | None = None) -> list[Choice]:
        from forms.models.field import Choice

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

    @admin.display(description="Title")
    def admin_get_title(self):
        return getattr_message_in_language(self, "title")

    @admin.display(description="Scope", ordering="universe__scope__slug")
    def admin_get_scope(self):
        return self.universe.scope.slug if self.universe and self.universe.scope else None

    @admin.display(description="Universe", ordering="universe__slug")
    def admin_get_universe(self):
        return self.universe.slug if self.universe else None

    @property
    def can_remove(self) -> bool:
        from forms.models.response_dimension_value import ResponseDimensionValue
        from program_v2.models.program_dimension_value import ProgramDimensionValue

        match self.universe.app:
            case "forms":
                return not ResponseDimensionValue.objects.filter(value__dimension=self).exists()
            case "program_v2":
                return not ProgramDimensionValue.objects.filter(value__dimension=self).exists()
            case _:
                raise NotImplementedError(self.universe.app)

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
