# Generated by Django 2.2.16 on 2020-12-27 14:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0008_auto_20200723_2058"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PaymentsEventMeta",
        ),
    ]
