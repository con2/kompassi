from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_auto_20151011_2005"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="muncipality",
            field=models.CharField(
                help_text="Virallinen kotikuntasi eli kunta jossa olet kirjoilla. Kotikunta ja v\xe4est\xf6rekisteriin merkityt etunimesi (kaikki) ovat pakollisia tietoja, mik\xe4li kuulut tai haluat liitty\xe4 johonkin yhdistykseen joka k\xe4ytt\xe4\xe4 t\xe4t\xe4 sivustoa\xa0j\xe4senrekisterin hallintaan.",
                max_length=127,
                verbose_name="Kotikunta",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
