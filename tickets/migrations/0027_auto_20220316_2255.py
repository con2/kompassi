# Generated by Django 2.2.27 on 2022-03-16 20:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0026_auto_20200723_1925"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="internal_description",
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=150),
        ),
    ]
