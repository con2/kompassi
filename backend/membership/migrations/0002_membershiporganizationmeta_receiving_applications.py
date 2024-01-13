from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="membershiporganizationmeta",
            name="receiving_applications",
            field=models.BooleanField(
                default=True,
                help_text="T\xe4m\xe4 asetus kontrolloi, voiko yhdistyksen j\xe4seneksi hakea suoraan Kompassin kautta.",
                verbose_name="Ottaa vastaan hakemuksia",
            ),
            preserve_default=True,
        ),
    ]
