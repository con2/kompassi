# Generated by Django 1.10.8 on 2017-11-12 21:51
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("badges", "0021_auto_20170830_2237"),
    ]

    operations = [
        migrations.AddField(
            model_name="badge",
            name="notes",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Internal notes are only visible to the event organizer. However, if the person in question requests a transcript of records, this field is also disclosed.",
                verbose_name="Internal notes",
            ),
        ),
    ]
