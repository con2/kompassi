# Generated by Django 5.0.8 on 2024-08-15 19:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0131_programmerole_override_perks_role_perks_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tag",
            name="public",
            field=models.BooleanField(default=True),
        ),
    ]
