from django.db import migrations


def default_to_program(apps, schema_editor):
    Universe = apps.get_model("dimensions", "Universe")
    Universe.objects.filter(
        slug="default",
        app="program_v2",
    ).update(
        slug="program",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("dimensions", "0003_remove_dimension_is_shown_to_subject_and_more"),
    ]

    operations = [
        migrations.RunPython(
            default_to_program,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.AlterUniqueTogether(
            name="universe",
            unique_together={("scope", "slug")},
        ),
    ]
