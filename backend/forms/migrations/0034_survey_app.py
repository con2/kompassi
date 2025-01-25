# Generated by Django 5.0.10 on 2025-01-25 14:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forms", "0033_survey_protect_responses"),
    ]

    operations = [
        migrations.AddField(
            model_name="survey",
            name="app",
            field=models.CharField(
                choices=[("forms", "Forms V2"), ("program_v2", "Program V2")],
                default="forms",
                help_text="Which app manages this survey?",
                max_length=10,
            ),
        ),
    ]