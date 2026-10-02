import logging

from django.db import migrations

logger = logging.getLogger(__name__)

# keep in sync with FieldType.can_propagate_to_annotation (frozen here so the migration stays stable)
PROPAGATABLE_TYPES = {
    "SingleLineText",
    "MultiLineText",
    "MarkdownText",
    "SingleCheckbox",
    "NumberField",
    "DecimalField",
    "DateField",
    "TimeField",
    "DateTimeField",
}


def propagate_form_fields_to_forms(apps, schema_editor):
    UniverseAnnotation = apps.get_model("dimensions", "UniverseAnnotation")
    Form = apps.get_model("forms", "Form")

    for universe_annotation in UniverseAnnotation.objects.exclude(form_fields=[]).select_related("annotation"):
        annotation_slug = universe_annotation.annotation.slug
        wanted_slugs = universe_annotation.form_fields

        for form in Form.objects.filter(survey__universe_id=universe_annotation.universe_id):
            changed = False
            for field_list in (form.fields, form.cached_enriched_fields):
                claimed = False
                # first wanted slug that exists in this form wins, as in the old extractor
                for wanted_slug in wanted_slugs:
                    for field in field_list:
                        if field.get("slug") != wanted_slug:
                            continue
                        if field.get("type") not in PROPAGATABLE_TYPES:
                            logger.warning(
                                "Form %s: field %s of type %s cannot propagate to annotation %s",
                                form.id,
                                wanted_slug,
                                field.get("type"),
                                annotation_slug,
                            )
                            continue
                        if claimed:
                            logger.warning(
                                "Form %s: field %s also fed annotation %s; only the first is kept",
                                form.id,
                                wanted_slug,
                                annotation_slug,
                            )
                            continue
                        field["propagateToAnnotation"] = annotation_slug
                        claimed = changed = True
            if changed:
                form.save(update_fields=["fields", "cached_enriched_fields"])


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("dimensions", "0019_rename_universe_app_name_to_app"),
        ("forms", "0058_survey_retention_period"),
    ]

    operations = [  # noqa: RUF012
        migrations.RunPython(propagate_form_fields_to_forms, migrations.RunPython.noop),
        migrations.RemoveField(model_name="universeannotation", name="form_fields"),
    ]
