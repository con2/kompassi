# Generated by Django 4.2.7 on 2023-11-21 19:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("solmukohta2024", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Technology",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.TextField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
