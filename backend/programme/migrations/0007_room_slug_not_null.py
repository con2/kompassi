import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0006_room_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="slug",
            field=models.CharField(
                default="",
                help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.',
                max_length=63,
                verbose_name="Tekninen nimi",
                validators=[
                    django.core.validators.RegexValidator(
                        regex="[a-z0-9-]+",
                        message="Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.",
                    )
                ],
            ),
            preserve_default=False,
        ),
    ]
