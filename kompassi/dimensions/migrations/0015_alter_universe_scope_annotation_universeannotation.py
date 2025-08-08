import django.db.models.deletion
import django_enum.fields
from django.db import migrations, models

from ..models.enums import AnnotationAppliesTo, AnnotationFlags


def populate_annotations(apps, schema_editor):
    OldAnnotation = apps.get_model("program_v2", "Annotation")
    EventAnnotation = apps.get_model("program_v2", "EventAnnotation")

    Universe = apps.get_model("dimensions", "Universe")
    Annotation = apps.get_model("dimensions", "Annotation")
    UniverseAnnotation = apps.get_model("dimensions", "UniverseAnnotation")

    Annotation.objects.bulk_create(
        [
            Annotation(
                slug=old_annotation.slug,
                title_en=old_annotation.title.get("en", ""),
                title_fi=old_annotation.title.get("fi", ""),
                title_sv=old_annotation.title.get("sv", ""),
                description_en=old_annotation.description.get("en", ""),
                description_fi=old_annotation.description.get("fi", ""),
                description_sv=old_annotation.description.get("sv", ""),
                type=old_annotation.type_slug,
                applies_to=AnnotationAppliesTo.from_kwargs(
                    is_applicable_to_involvements=False,
                    is_applicable_to_program_items=old_annotation.is_applicable_to_program_items,
                    is_applicable_to_schedule_items=old_annotation.is_applicable_to_schedule_items,
                ).value,
                flags=AnnotationFlags.from_kwargs(
                    is_public=old_annotation.is_public,
                    is_shown_in_detail=old_annotation.is_shown_in_detail,
                    is_computed=old_annotation.is_computed,
                    is_perk=False,
                ).value,
            )
            for old_annotation in OldAnnotation.objects.all()
        ],
        batch_size=400,
    )

    program_universes_by_event_slug = {univ.scope.slug: univ for univ in Universe.objects.filter(slug="program")}
    annotations_by_slug = {ann.slug: ann for ann in Annotation.objects.all()}

    UniverseAnnotation.objects.bulk_create(
        [
            UniverseAnnotation(
                universe=program_universes_by_event_slug[ea.meta.event.slug],
                annotation=annotations_by_slug[ea.annotation.slug],
                is_active=ea.is_active,
                form_fields=ea.program_form_fields,
            )
            for ea in EventAnnotation.objects.all()
        ],
        batch_size=400,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("dimensions", "0014_alter_dimension_can_values_be_added"),
        ("program_v2", "0045_programv2eventmeta_konsti_url_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="universe",
            name="scope",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="universes", to="dimensions.scope"
            ),
        ),
        migrations.CreateModel(
            name="Annotation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(unique=True)),
                ("title_en", models.TextField(blank=True, default="")),
                ("title_fi", models.TextField(blank=True, default="")),
                ("title_sv", models.TextField(blank=True, default="")),
                ("description_en", models.TextField(blank=True, default="")),
                ("description_fi", models.TextField(blank=True, default="")),
                ("description_sv", models.TextField(blank=True, default="")),
                (
                    "type",
                    django_enum.fields.EnumCharField(
                        choices=[("string", "STRING"), ("number", "NUMBER"), ("boolean", "BOOLEAN")], max_length=7
                    ),
                ),
                (
                    "applies_to",
                    django_enum.fields.SmallIntegerFlagField(
                        blank=True,
                        choices=[(0, "NOTHING"), (1, "PROGRAM_ITEM"), (2, "SCHEDULE_ITEM"), (4, "INVOLVEMENT")],
                        default=1,
                    ),
                ),
                (
                    "flags",
                    django_enum.fields.SmallIntegerFlagField(
                        blank=True,
                        choices=[(0, "NONE"), (1, "PUBLIC"), (2, "SHOWN_IN_DETAIL"), (4, "COMPUTED"), (8, "PERK")],
                        default=1,
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(("type__in", ["string", "number", "boolean"])),
                        name="dimensions_Annotation_type_AnnotationDataType",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(
                            models.Q(("applies_to__gte", 0), ("applies_to__lte", 7)), ("applies_to", 0), _connector="OR"
                        ),
                        name="dimensions_Annotation_applies_to_AnnotationAppliesTo",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(
                            models.Q(("flags__gte", 0), ("flags__lte", 15)), ("flags", 0), _connector="OR"
                        ),
                        name="dimensions_Annotation_flags_AnnotationFlags",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="UniverseAnnotation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_active", models.BooleanField(default=True)),
                (
                    "form_fields",
                    models.JSONField(default=dict, help_text="Slugs of form fields to extract values from."),
                ),
                (
                    "annotation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="all_universe_annotations",
                        to="dimensions.annotation",
                    ),
                ),
                (
                    "universe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="all_universe_annotations",
                        to="dimensions.universe",
                    ),
                ),
            ],
            options={
                "unique_together": {("universe", "annotation")},
            },
        ),
        migrations.RunPython(
            populate_annotations,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
    ]
