import django.contrib.postgres.fields
from django.db import migrations, models


def backfill_is_key_field(apps, schema_editor):
    """
    cached_key_fields used to be an authoritative, directly-edited list of field slugs.
    It is now denormalized from the isKeyField flag of the form fields. Backfill that flag
    into existing form fields so a later form edit does not wipe existing key fields.
    """
    Survey = apps.get_model("forms", "Survey")

    for survey in Survey.objects.exclude(cached_key_fields=[]).prefetch_related("languages"):
        key_field_slugs = set(survey.cached_key_fields)
        for form in survey.languages.all():
            changed = False
            for field_list in (form.fields, form.cached_enriched_fields):
                for field in field_list:
                    if field.get("slug") in key_field_slugs and not field.get("isKeyField"):
                        field["isKeyField"] = True
                        changed = True
            if changed:
                form.save(update_fields=["fields", "cached_enriched_fields"])


class Migration(migrations.Migration):
    dependencies = [
        ("forms", "0054_projection_special_fields"),
    ]

    operations = [
        migrations.RenameField(
            model_name="survey",
            old_name="key_fields",
            new_name="cached_key_fields",
        ),
        migrations.AlterField(
            model_name="survey",
            name="cached_key_fields",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255),
                blank=True,
                default=list,
                help_text=(
                    "Key fields will be shown in the response list. "
                    "This field is denormalized from the isKeyField flag of the form fields "
                    "and should not be edited directly."
                ),
                size=None,
                verbose_name="key fields",
            ),
        ),
        migrations.RunPython(
            code=backfill_is_key_field,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
    ]
