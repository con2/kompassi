"""
Manual overrides for automatically computed perks.

Perks (free entry, meal vouchers, swag, shirts etc.) are computed automatically by
event-specific Emperkelators (see ``emperkelators/``) and stored on a person's
``COMBINED_PERKS`` Involvement as dimension values and annotation values.

An Involvement admin may manually override individual perks. Which perks are overridden
is tracked by the values of a technical Involvement dimension ``manual-perks-override``:

* a dimension perk ``ticket-type`` is overridden by the value ``d-ticket-type``
* an annotation perk ``tracon:mealVouchers`` is overridden by the value ``a-tracon-meal-vouchers``
  (colon -> ``-``, camelCase -> kebab-case, lowercased)

The values of ``manual-perks-override`` are created on demand, as the set of perk
dimensions/annotations may be edited by the admin.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from kompassi.dimensions.models.dimension_dto import DimensionDTO
from kompassi.dimensions.models.enums import AnnotationAppliesTo, AnnotationFlags, ValueOrdering
from kompassi.dimensions.models.universe import Universe

MANUAL_PERKS_OVERRIDE_SLUG = "manual-perks-override"

# Matches the position right before an uppercase letter (not at the start of the string).
_CAMEL_BOUNDARY = re.compile(r"(?<!^)(?=[A-Z])")


def dimension_override_value(dimension_slug: str) -> str:
    """e.g. ``ticket-type`` -> ``d-ticket-type``"""
    return f"d-{dimension_slug}"


def annotation_override_value(annotation_slug: str) -> str:
    """e.g. ``tracon:mealVouchers`` -> ``a-tracon-meal-vouchers``"""
    kebab = _CAMEL_BOUNDARY.sub("-", annotation_slug.replace(":", "-")).lower()
    return f"a-{kebab}"


@dataclass(frozen=True)
class PerkKey:
    override_value: str
    kind: Literal["dimension", "annotation"]
    slug: str


def get_perk_keys(universe: Universe) -> dict[str, PerkKey]:
    """
    Return a mapping ``override_value -> PerkKey`` for every overridable perk in the universe.

    Perks are:

    * every ``is_technical=False`` dimension (technical dimensions such as
      ``app``/``type``/``state``/``registry``/``manual-perks-override`` are excluded), and
    * every annotation applicable to involvements that is a perk but not computed.

    The kebab-casing of annotation slugs is lossy, so we never reverse it: instead we
    iterate forward over the schema and build the lookup from the canonical slug.
    """
    perk_keys: dict[str, PerkKey] = {}

    for dimension_slug in universe.dimensions.filter(is_technical=False).values_list("slug", flat=True):
        override_value = dimension_override_value(dimension_slug)
        perk_keys[override_value] = PerkKey(override_value, "dimension", dimension_slug)

    perk_annotations = (
        universe.annotations.filter(
            applies_to__has_all=AnnotationAppliesTo.INVOLVEMENT,
            flags__has_all=AnnotationFlags.PERK,
        )
        .exclude(flags__has_all=AnnotationFlags.COMPUTED)
        .values_list("slug", flat=True)
    )
    for annotation_slug in perk_annotations:
        override_value = annotation_override_value(annotation_slug)
        perk_keys[override_value] = PerkKey(override_value, "annotation", annotation_slug)

    return perk_keys


def get_manual_perks_override_dimension() -> DimensionDTO:
    """
    The technical dimension that tracks which perks are manually overridden.

    Values are created on demand (no static ``choices``).
    """
    return DimensionDTO(
        slug=MANUAL_PERKS_OVERRIDE_SLUG,
        title=dict(
            en="Manually overridden perks",
            fi="Käsin ylikirjoitetut edut",
            sv="Manuellt åsidosatta förmåner",
        ),
        is_public=False,
        is_key_dimension=False,
        is_multi_value=True,
        is_technical=True,
        can_values_be_added=False,
        is_list_filter=False,
        is_shown_in_detail=False,
        is_negative_selection=False,
        value_ordering=ValueOrdering.TITLE,
        order=9100,
    )
