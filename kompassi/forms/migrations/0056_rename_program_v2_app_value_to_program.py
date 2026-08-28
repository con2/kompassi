from django.db import migrations


def rename_program_v2_to_program(apps, schema_editor):
    Survey = apps.get_model("forms", "Survey")
    Survey.objects.filter(app_name="program_v2").update(app_name="program")


def rename_program_to_program_v2(apps, schema_editor):
    Survey = apps.get_model("forms", "Survey")
    Survey.objects.filter(app_name="program").update(app_name="program_v2")


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("forms", "0055_rename_survey_key_fields_cached_key_fields"),
    ]

    operations = [  # noqa: RUF012
        migrations.RunPython(
            rename_program_v2_to_program,
            rename_program_to_program_v2,
            elidable=True,
        ),
    ]
