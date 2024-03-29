# Generated by Django 4.2.1 on 2023-09-05 05:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0037_alter_organization_panel_css_class"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="discord_handle",
            field=models.CharField(
                blank=True,
                help_text="Your Discord username (NOTE: not display name). Events may use this to give you roles based on your participation.",
                max_length=63,
                verbose_name="Discord username",
            ),
        ),
    ]
