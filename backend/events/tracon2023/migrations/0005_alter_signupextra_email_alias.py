# Generated by Django 5.0.9 on 2024-11-30 15:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracon2023", "0004_delete_signupextraafterpartyproxy"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupextra",
            name="email_alias",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Coniitit saavat käyttöönsä nick@tracon.fi-tyyppisen sähköpostialiaksen, joka ohjataan coniitin omaan sähköpostilaatikkoon. Tässä voit toivoa haluamaasi sähköpostialiaksen alkuosaa eli sitä, joka tulee ennen @tracon.fi:tä. Sallittuja merkkejä ovat pienet kirjaimet a-z, numerot 0-9 sekä väliviiva.",
                max_length=32,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.",
                        regex="^[a-z0-9-]+$",
                    )
                ],
                verbose_name="Sähköpostialias",
            ),
        ),
    ]
