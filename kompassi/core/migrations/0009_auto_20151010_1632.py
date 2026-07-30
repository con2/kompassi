from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("core", "0008_person_muncipality"),
    ]

    operations = [  # noqa: RUF012
        migrations.AlterField(
            model_name="person",
            name="muncipality",
            field=models.CharField(
                help_text="Virallinen kotikuntasi eli kunta jossa olet kirjoilla.",
                max_length=127,
                verbose_name="Kotikunta",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
