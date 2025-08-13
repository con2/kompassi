from __future__ import annotations

from django.db import models

from kompassi.core.utils.model_utils import slugify_underscore
from kompassi.reports.models.column import Column
from kompassi.reports.models.enums import TypeOfColumn
from kompassi.reports.models.report import Report

from ..models.dimension import Dimension
from ..models.universe import Universe

DEFAULT_TITLE_PREFIXES = {
    "en": "Dimension: ",
    "fi": "Dimensio: ",
    "sv": "Dimension: ",
}


def get_dimension_report(
    dimension: Dimension,
    subject_dimension_values: models.QuerySet,
    lang: str,
    title_prefixes: dict[str, str] | None = None,
) -> Report:
    """
    subject_dimension_values must be a queryset of a SubjectDimensionValue model
    """
    if title_prefixes is None:
        title_prefixes = DEFAULT_TITLE_PREFIXES

    # NOTE: empty order_by is intentional
    # see https://docs.djangoproject.com/en/5.2/topics/db/aggregation/#interaction-with-order-by
    rows = (
        subject_dimension_values.filter(value__dimension=dimension)
        .values(value_slug=models.F("value__slug"))
        .annotate(count=models.Count("id"))
        .order_by()
    )

    ordered_values = dimension.get_values(lang)
    values_by_slug = {value.slug: value for value in ordered_values}
    count_by_value_slug = {row["value_slug"]: row["count"] for row in rows}
    rows = [
        [values_by_slug[value.slug].get_title(lang), count_by_value_slug.get(value.slug, 0)] for value in ordered_values
    ]

    slug = f"dimension_{slugify_underscore(dimension.slug)}"
    return Report(
        slug=slug,
        title={
            lang: title_prefixes[lang] + title_in_language for (lang, title_in_language) in dimension.title_dict.items()
        },
        columns=[
            Column(
                slug="value_title",
                title=dict(
                    en="Value",
                    fi="Arvo",
                    sv="Värde",
                ),
                type=TypeOfColumn.STRING,
            ),
            Column(
                slug="count",
                title=dict(
                    en="Count",
                    fi="Lukumäärä",
                    sv="Antal",
                ),
                type=TypeOfColumn.INT,
            ),
        ],
        rows=rows,
        has_total_row=True,
    )


def get_dimension_reports(SubjectDimensionValue: type[models.Model], universe: Universe, lang: str):
    return [
        get_dimension_report(
            dimension=dimension,
            subject_dimension_values=SubjectDimensionValue.objects.filter(value__dimension__universe=universe),
            lang=lang,
        )
        for dimension in universe.dimensions.all()
    ]
