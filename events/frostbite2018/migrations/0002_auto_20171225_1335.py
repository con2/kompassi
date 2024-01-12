# Generated by Django 1.10.8 on 2017-12-25 11:35
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("frostbite2018", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupextra",
            name="shirt_type",
            field=models.CharField(
                choices=[
                    ("STAFF", "Staff"),
                    ("DESURITY", "Desurity"),
                    ("KUVAAJA", "Kuvaaja"),
                    ("VENDOR", "Myynti"),
                    ("TOOLATE", "Myöhästyi paitatilauksesta"),
                ],
                default="TOOLATE",
                max_length=8,
                verbose_name="Paidan tyyppi",
            ),
        ),
    ]
