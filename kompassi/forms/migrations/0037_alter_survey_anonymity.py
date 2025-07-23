from django.db import migrations, models
from django.db.models import F
from django.db.models.functions import Upper


def uppercase_anomumity_choices(apps, schema_editor):
    Survey = apps.get_model("forms", "Survey")
    Survey.objects.all().update(anonymity=Upper(F("anonymity")))


class Migration(migrations.Migration):
    dependencies = [
        ("forms", "0036_alter_form_unique_together_remove_survey_languages_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="survey",
            name="anonymity",
            field=models.CharField(
                choices=[
                    ("HARD", "Hard anonymous"),
                    ("SOFT", "Soft anonymous (linked to user account but not shown to survey owner)"),
                    ("NAME_AND_EMAIL", "Name and email shown to survey owner if responded logged-in"),
                ],
                default="SOFT",
                help_text="Hard anonymous: responses are not linked to user accounts and IP addresses are not recorded. Soft anonymous: responses are linked to user accounts but not shown to survey owners. Name and email: responses are linked to user accounts and shown to survey owners.",
                max_length=14,
                verbose_name="anonymity",
            ),
        ),
        migrations.RunPython(
            uppercase_anomumity_choices,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
    ]
