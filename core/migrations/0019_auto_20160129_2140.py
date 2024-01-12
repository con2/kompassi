# Generated by Django 1.9.1 on 2016-01-29 19:40


from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0018_auto_20160124_1447"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="first_name",
            field=models.CharField(max_length=1023, verbose_name="First name"),
        ),
        migrations.AlterField(
            model_name="person",
            name="nick",
            field=models.CharField(blank=True, help_text="Nick name", max_length=1023),
        ),
        migrations.AlterField(
            model_name="person",
            name="official_first_names",
            field=models.CharField(blank=True, max_length=1023, verbose_name="Official first names"),
        ),
        migrations.AlterField(
            model_name="person",
            name="surname",
            field=models.CharField(max_length=1023, verbose_name="Surname"),
        ),
    ]
