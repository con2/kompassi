# Generated by Django 5.0.1 on 2024-01-24 11:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forms", "0020_form_cached_enriched_fields_alter_form_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="dimension",
            name="is_multi_value",
            field=models.BooleanField(
                default=False,
                help_text="Multi-value dimensions allow multiple values to be selected. NOTE: In the database, all dimensions are multi-value, so this is just a UI hint.",
            ),
        ),
    ]
