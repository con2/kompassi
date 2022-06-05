from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("traconx", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="signupextra",
            name="email_alias",
            field=models.CharField(
                default="",
                validators=[
                    django.core.validators.RegexValidator(
                        regex="[a-z0-9-]+",
                        message="Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.",
                    )
                ],
                max_length=32,
                blank=True,
                help_text="Coniitit saavat k\xe4ytt\xf6\xf6ns\xe4 nick@tracon.fi-tyyppisen s\xe4hk\xf6postialiaksen, joka ohjataan coniitin omaan s\xe4hk\xf6postilaatikkoon. T\xe4ss\xe4 voit toivoa haluamaasi s\xe4hk\xf6postialiasta. Sallittuja merkkej\xe4 ovat pienet kirjaimet a-z, numerot 0-9 sek\xe4 v\xe4liviiva.",
                verbose_name="S\xe4hk\xf6postialias",
            ),
            preserve_default=True,
        ),
    ]
