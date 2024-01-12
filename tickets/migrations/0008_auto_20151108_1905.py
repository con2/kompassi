from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0007_accommodation_v3"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accommodationinformation",
            name="email",
            field=models.EmailField(
                default="", max_length=254, verbose_name="S\xc3\xa4hk\xc3\xb6postiosoite", blank=True
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="email",
            field=models.EmailField(
                help_text="Tarkista s\xe4hk\xf6postiosoite huolellisesti. Tilausvahvistus sek\xe4 mahdolliset s\xe4hk\xf6iset liput l\xe4hetet\xe4\xe4n t\xe4h\xe4n s\xe4hk\xf6postiosoitteeseen. HUOM! Hotmail-osoitteiden kanssa on v\xe4lill\xe4 ollut viestien perillemeno-ongelmia. Suosittelemme k\xe4ytt\xe4m\xe4\xe4n jotain muuta s\xe4hk\xf6postiosoitetta kuin Hotmailia.",
                max_length=254,
                verbose_name="S\xe4hk\xf6postiosoite",
            ),
        ),
    ]
