# Generated by Django 5.0.2 on 2024-02-23 17:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forms", "0023_response_sequence_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="form",
            name="title",
            field=models.CharField(default="", max_length=255),
        ),
    ]
