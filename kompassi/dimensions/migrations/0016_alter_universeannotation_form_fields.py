from django.db import migrations, models


def fix_form_fields(apps, schema_editor):
    UniverseAnnotation = apps.get_model("dimensions", "UniverseAnnotation")
    for annotation in UniverseAnnotation.objects.all():
        if not isinstance(annotation.form_fields, list):
            annotation.form_fields = []
            annotation.save()


class Migration(migrations.Migration):
    dependencies = [
        ("dimensions", "0015_alter_universe_scope_annotation_universeannotation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="universeannotation",
            name="form_fields",
            field=models.JSONField(
                default=list,
                help_text="Slugs of form fields to extract values from.",
            ),
        ),
        migrations.RunPython(fix_form_fields, reverse_code=migrations.RunPython.noop, elidable=True),
    ]
