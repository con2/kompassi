# Generated by Django 4.2.6 on 2023-11-09 06:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forms", "0009_remove_eventform_active_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventform",
            name="thank_you_message",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="globalform",
            name="thank_you_message",
            field=models.TextField(blank=True, default=""),
        ),
    ]
