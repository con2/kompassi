from django.db import migrations


def set_program_form_attributes(apps, schema_editor):
    """
    These fields are now set by the createProgramForm mutation,
    but they were missing from the first versions and there may be
    program forms out there without these attributes set.
    """
    Survey = apps.get_model("forms", "Survey")
    Survey.objects.filter(app="program_v2").update(
        login_required=True,
        anonymity="name_and_email",
        key_fields=["title"],
    )


class Migration(migrations.Migration):
    dependencies = [
        ("program_v2", "0030_delete_offerform"),
        ("forms", "0036_alter_form_unique_together_remove_survey_languages_and_more"),
    ]

    operations = [
        migrations.RunPython(
            code=set_program_form_attributes,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        )
    ]
