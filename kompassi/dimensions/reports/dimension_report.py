from __future__ import annotations

from django.db import models

from kompassi.core.utils.model_utils import slugify_underscore
from kompassi.reports.models.column import Column
from kompassi.reports.models.enums import TypeOfColumn
from kompassi.reports.models.report import Report

from ..models.dimension import Dimension
from ..models.universe import Universe


def dimension_report(SubjectDimensionValue: type[models.Model], dimension: Dimension, lang: str):
    # NOTE: empty order_by is intentional
    # see https://docs.djangoproject.com/en/5.2/topics/db/aggregation/#interaction-with-order-by
    rows = (
        SubjectDimensionValue.objects.filter(value__dimension=dimension)
        .values(value_slug=models.F("value__slug"))
        .annotate(count=models.Count("id"))
        .order_by()
    )

    slug = f"dimension_{slugify_underscore(dimension.slug)}"
    return Report(
        slug=slug,
        title=dimension.title_dict,
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
            # Column(
            #     slug="percentage",
            #     title=dict(
            #         en="Percentage",
            #         fi="Prosenttiosuus",
            #         sv="Procent",
            #     ),
            #     type=TypeOfColumn.STRING,
            # ),
        ],
        rows=[[row["value_slug"], row["count"]] for row in rows],
        has_total_row=True,
    )


def get_dimension_reports(SubjectDimensionValue: type[models.Model], universe: Universe, lang: str):
    return [dimension_report(SubjectDimensionValue, dimension, lang) for dimension in universe.dimensions.all()]
