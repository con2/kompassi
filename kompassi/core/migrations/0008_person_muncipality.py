from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("core", "0007_organization_logo_url"),
    ]

    operations = [  # noqa: RUF012
        migrations.AddField(
            model_name="person",
            name="muncipality",
            field=models.EmailField(
                help_text="Virallinen kotikuntasi eli kunta jossa olet kirjoilla.",
                max_length=127,
                verbose_name="Kotikunta",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
