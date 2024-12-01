from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import migrations

if TYPE_CHECKING:
    pass


def old_value_ordering_to_new(old_value_ordering: str) -> int:
    """
    See dimensions/models/value_ordering.py:ValueOrdering
    """
    match old_value_ordering:
        case "manual":
            return 1
        case "slug":
            return 2
        case "title":
            return 3
        case _:
            raise ValueError(f"Invalid ValueOrdering slug: {old_value_ordering}")


def populate_from_forms(apps, schema_editor):
    Scope = apps.get_model("dimensions", "Scope")
    Universe = apps.get_model("dimensions", "Universe")
    Dimension = apps.get_model("dimensions", "Dimension")
    DimensionValue = apps.get_model("dimensions", "DimensionValue")

    Survey = apps.get_model("forms", "Survey")

    for survey in Survey.objects.all():
        scope, _ = Scope.objects.get_or_create(
            slug=survey.event.slug,
            defaults=dict(
                name=survey.event.name,
                event=survey.event,
                organization=survey.event.organization,
            ),
        )

        universe = Universe.objects.create(
            scope=scope,
            app="forms",
            slug=survey.slug,
        )

        survey_dimensions = list(survey.dimensions.all())
        dimensions = Dimension.objects.bulk_create(
            (
                Dimension(
                    universe=universe,
                    slug=survey_dimension.slug,
                    title_en=survey_dimension.title.get("en", ""),
                    title_fi=survey_dimension.title.get("fi", ""),
                    title_sv=survey_dimension.title.get("sv", ""),
                    order=survey_dimension.order,
                    is_key_dimension=survey_dimension.is_key_dimension,
                    is_multi_value=survey_dimension.is_multi_value,
                    is_shown_to_subject=survey_dimension.is_shown_to_respondent,
                )
                for survey_dimension in survey_dimensions
            ),
            batch_size=400,
        )

        DimensionValue.objects.bulk_create(
            (
                DimensionValue(
                    dimension=dimension,
                    slug=value.slug,
                    title_en=value.title.get("en", ""),
                    title_fi=value.title.get("fi", ""),
                    title_sv=value.title.get("sv", ""),
                    color=value.color,
                    is_initial=value.is_initial,
                )
                for survey_dimension, dimension in zip(survey_dimensions, dimensions, strict=True)
                for value in survey_dimension.values.all()
            ),
            batch_size=400,
        )


def populate_from_program_v2(apps, schema_editor):
    Scope = apps.get_model("dimensions", "Scope")
    Universe = apps.get_model("dimensions", "Universe")
    Dimension = apps.get_model("dimensions", "Dimension")
    DimensionValue = apps.get_model("dimensions", "DimensionValue")

    ProgramV2EventMeta = apps.get_model("program_v2", "ProgramV2EventMeta")
    ProgramDimension = apps.get_model("program_v2", "Dimension")

    for meta in ProgramV2EventMeta.objects.all():
        scope, _ = Scope.objects.get_or_create(
            slug=meta.event.slug,
            defaults=dict(
                name=meta.event.name,
                event=meta.event,
                organization=meta.event.organization,
            ),
        )

        universe = Universe.objects.create(
            scope=scope,
            app="program_v2",
            slug="default",
        )

        program_dimensions = list(ProgramDimension.objects.filter(event=meta.event))

        dimensions = Dimension.objects.bulk_create(
            (
                Dimension(
                    universe=universe,
                    slug=program_dimension.slug,
                    title_en=program_dimension.title.get("en", ""),
                    title_fi=program_dimension.title.get("fi", ""),
                    title_sv=program_dimension.title.get("sv", ""),
                    order=program_dimension.order,
                    is_multi_value=program_dimension.is_multi_value,
                    is_list_filter=program_dimension.is_list_filter,
                    is_shown_in_detail=program_dimension.is_shown_in_detail,
                    is_negative_selection=program_dimension.is_negative_selection,
                    value_ordering=old_value_ordering_to_new(program_dimension.value_ordering),
                )
                for program_dimension in program_dimensions
            ),
            batch_size=400,
        )

        DimensionValue.objects.bulk_create(
            (
                DimensionValue(
                    dimension=dimension,
                    slug=value.slug,
                    title_en=value.title.get("en", ""),
                    title_fi=value.title.get("fi", ""),
                    title_sv=value.title.get("sv", ""),
                    color=value.color,
                    order=value.order,
                )
                for program_dimension, dimension in zip(program_dimensions, dimensions, strict=True)
                for value in program_dimension.values.all()
            ),
            batch_size=400,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("forms", "0029_formseventmeta"),
        ("program_v2", "0025_scheduleitem_created_at_scheduleitem_updated_at"),
        ("dimensions", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            populate_from_forms,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.RunPython(
            populate_from_program_v2,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
    ]
