from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0003_programme_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="programme",
            name="state",
            field=models.CharField(
                default="accepted",
                help_text='Tilassa "Julkaistu" olevat ohjelmat n\xe4kyv\xe4t ohjelmakartassa, jos ohjelmakartta on julkinen.',
                max_length=15,
                verbose_name="Ohjelmanumeron tila",
                choices=[
                    ("idea", "Ideoitu sis\xe4isesti"),
                    ("asked", "Kysytty ohjelmanj\xe4rjest\xe4j\xe4lt\xe4"),
                    ("offered", "Ohjelmatarjous vastaanotettu"),
                    ("accepted", "Hyv\xe4ksytty"),
                    ("published", "Julkaistu"),
                    ("cancelled", "Peruutettu"),
                    ("rejected", "Hyl\xe4tty"),
                ],
            ),
            preserve_default=True,
        ),
    ]
