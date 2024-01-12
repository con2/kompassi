# Generated by Django 2.2.9 on 2020-01-22 20:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0095_auto_20190919_2136"),
    ]

    operations = [
        migrations.AlterField(
            model_name="alternativeprogrammeform",
            name="title",
            field=models.CharField(
                help_text="This title is visible to the programme host.", max_length=1023, verbose_name="title"
            ),
        ),
    ]
