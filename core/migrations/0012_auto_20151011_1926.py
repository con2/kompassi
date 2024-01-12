from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_organization_muncipality"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="official_first_names",
            field=models.CharField(
                help_text="Tarpeellinen, jos kuulut tai haluat liitty\xe4 johonkin yhdistykseen joka k\xe4ytt\xe4\xe4 {\xa0kompassia }\xa0j\xe4senrekisterin hallintaan.",
                max_length=1023,
                verbose_name="Viralliset etunimet",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="person",
            name="first_name",
            field=models.CharField(max_length=1023, verbose_name="Kutsumanimi"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="person",
            name="muncipality",
            field=models.CharField(
                help_text="Virallinen kotikuntasi eli kunta jossa olet kirjoilla. Tarpeellinen, jos kuulut tai haluat liitty\xe4 johonkin yhdistykseen joka k\xe4ytt\xe4\xe4 {\xa0kompassia }\xa0j\xe4senrekisterin hallintaan.",
                max_length=127,
                verbose_name="Kotikunta",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
