from django.db import migrations


def rename_program_v2_to_program(apps, schema_editor):
    Universe = apps.get_model("dimensions", "Universe")
    Universe.objects.filter(app_name="program_v2").update(app_name="program")


def rename_program_to_program_v2(apps, schema_editor):
    Universe = apps.get_model("dimensions", "Universe")
    Universe.objects.filter(app_name="program").update(app_name="program_v2")


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("dimensions", "0017_remove_annotation_dimensions_annotation_type_annotationdatatype_and_more"),
    ]

    operations = [  # noqa: RUF012
        migrations.RunPython(
            rename_program_v2_to_program,
            rename_program_to_program_v2,
            elidable=True,
        ),
    ]
