# Generated by Django 5.1.5 on 2025-04-18 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forms", "0038_survey_created_at_survey_created_by_and_more"),
        ("program_v2", "0032_remove_programv2eventmeta_skip_offer_form_selection"),
    ]

    operations = [
        migrations.AddField(
            model_name="program",
            name="program_offer",
            field=models.ForeignKey(
                blank=True,
                help_text="If this program was created from a program offer, this field will be set to the program offer.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="programs",
                to="forms.response",
            ),
        ),
        migrations.AlterField(
            model_name="program",
            name="cached_dimensions",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
