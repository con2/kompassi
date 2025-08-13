from __future__ import annotations

from kompassi.dimensions.models.universe import Universe
from kompassi.dimensions.reports.dimension_reports import get_dimension_report
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.models.report import Report

from ..models.enums import InvolvementType
from ..models.involvement_dimension_value import InvolvementDimensionValue

COMBINED_PERKS = dict(
    en="Combined perks: ",
    fi="Yhdistetyt edut: ",
    sv="Kombinerade förmåner: ",
)
EXCLUDED_DIMENSION_SLUGS = {"app", "registry", "type", "state"}


def get_combined_perks_reports(universe: Universe, lang: str = DEFAULT_LANGUAGE) -> list[Report]:
    cache = universe.preload_dimensions()
    idvs = InvolvementDimensionValue.objects.filter(
        value__dimension__universe=universe,
        subject__type=InvolvementType.COMBINED_PERKS,
        subject__is_active=True,
    ).exclude(
        value__dimension__slug__in=EXCLUDED_DIMENSION_SLUGS,
    )
    dimension_slugs = (
        idvs.values_list("value__dimension__slug", flat=True).distinct().order_by("value__dimension__slug")
    )

    return [
        get_dimension_report(dimension, idvs.filter(value__dimension=dimension), lang, title_prefixes=COMBINED_PERKS)
        for dimension_slug in dimension_slugs
        if (dimension := cache.dimensions.get(dimension_slug))
    ]
