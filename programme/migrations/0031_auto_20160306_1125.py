# Generated by Django 1.9.1 on 2016-03-06 09:25


from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0030_auto_20160305_1902"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ProgrammeProfileProxy",
        ),
        migrations.AlterModelOptions(
            name="programmerole",
            options={"verbose_name": "Programme host", "verbose_name_plural": "Programme hosts"},
        ),
    ]
