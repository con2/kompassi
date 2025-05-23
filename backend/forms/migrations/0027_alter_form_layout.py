# Generated by Django 5.0.9 on 2024-10-18 16:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forms", "0026_survey_subscribers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="form",
            name="layout",
            field=models.CharField(
                choices=[("vertical", "Vertical"), ("horizontal", "Horizontal")],
                default="vertical",
                max_length=10,
                verbose_name="Layout",
            ),
        ),
    ]
