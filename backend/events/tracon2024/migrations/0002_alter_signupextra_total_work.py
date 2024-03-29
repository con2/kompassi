# Generated by Django 4.2.9 on 2024-01-14 17:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracon2024", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signupextra",
            name="total_work",
            field=models.CharField(
                choices=[
                    ("10h", "10h minimi - 2 ruokalippua, 1 työvoimatuote"),
                    ("12h", "12h - 3 ruokalippua, 1 työvoimatuote"),
                    ("14h", "14h - 3 ruokalippua, 2 työvoimatuotetta"),
                    ("16h", "16h - 4 ruokalippua, 2 työvoimatuotetta"),
                ],
                help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Minimi on pääsääntöisesti kymmenen tuntia.",
                max_length=15,
                verbose_name="Toivottu kokonaistyömäärä",
            ),
        ),
    ]
