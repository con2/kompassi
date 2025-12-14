from kompassi.core.models.event import Event
from kompassi.graphql_api.language import DEFAULT_LANGUAGE
from kompassi.reports.models.enums import TypeOfColumn
from kompassi.reports.models.report import Column, Report

from ..models.enums import InvolvementType

TITLE = dict(
    en="Shirt sizes by shirt type",
    fi="T-paitakoot paidan tyypin mukaan",
    sv="T-tröjstorlekar efter t-tröjtyp",
)


def get_shirt_sizes_by_shirt_type_report(event: Event, lang: str = DEFAULT_LANGUAGE) -> Report:
    """
    For an event that has shirt-size and shirt-type involvement dimensions,
    generate a report showing shirt types as columns and shirt sizes as rows,
    with counts of active involvements in each cell.
    """

    meta = event.involvement_event_meta
    if meta is None:
        raise ValueError("Event does not have involvement event meta")

    shirt_size_dimension = meta.universe.dimensions.get(slug="shirt-size")
    shirt_type_dimension = meta.universe.dimensions.get(slug="shirt-type")

    shirt_size_choices = shirt_size_dimension.get_values(lang)
    shirt_type_choices = shirt_type_dimension.get_values(lang)

    # type -> size -> count
    results: dict[str, dict[str, int]] = {}

    for cached_dimensions in meta.active_involvements.filter(
        type=InvolvementType.COMBINED_PERKS,
    ).values_list(
        "cached_dimensions",
        flat=True,
    ):
        shirt_size_values = cached_dimensions.get("shirt-size", [])
        shirt_type_values = cached_dimensions.get("shirt-type", [])
        for shirt_type in shirt_type_values:
            for shirt_size in shirt_size_values:
                results.setdefault(shirt_type, {}).setdefault(shirt_size, 0)
                results[shirt_type][shirt_size] += 1

    # remove the "No shirt" shirt size if present
    shirt_size_choices = [size_dv for size_dv in shirt_size_choices if size_dv.slug not in {"no-shirt", "none"}]

    # remove all zero columns
    shirt_type_choices = [
        shirt_type_dv
        for shirt_type_dv in shirt_type_choices
        if any(results.get(shirt_type_dv.slug, {}).get(size_dv.slug, 0) > 0 for size_dv in shirt_size_choices)
    ]

    return Report(
        slug="shirt-sizes-by-shirt-type",
        title=TITLE,
        has_total_row=True,
        columns=[
            Column(
                slug="size",
                title=shirt_size_dimension.title_dict,
                type=TypeOfColumn.INT,
            ),
            *[
                Column(
                    slug=shirt_type_dv.slug,
                    title=shirt_type_dv.title_dict,
                    type=TypeOfColumn.INT,
                )
                for shirt_type_dv in shirt_type_choices
            ],
        ],
        rows=[
            [
                size_dv.get_title(lang),
                *(results.get(shirt_type_dv.slug, {}).get(size_dv.slug, 0) for shirt_type_dv in shirt_type_choices),
            ]
            for size_dv in shirt_size_choices
        ],
    )
