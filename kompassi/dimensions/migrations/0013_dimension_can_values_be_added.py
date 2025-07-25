# Generated by Django 5.2.4 on 2025-07-26 09:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dimensions", "0012_universe_app_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="dimension",
            name="can_values_be_added",
            field=models.BooleanField(
                default=True,
                help_text="If set, users can add values to this dimension in the UI. Some technical dimensions may allow adding values and some may not.",
            ),
        ),
    ]
