# Generated by Django 2.2.24 on 2021-10-19 19:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("listings", "0005_externalevent_cancelled"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listing",
            name="events",
        ),
        migrations.RemoveField(
            model_name="listing",
            name="external_events",
        ),
    ]
