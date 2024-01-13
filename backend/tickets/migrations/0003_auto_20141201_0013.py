from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0002_ticketseventmeta_front_page_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="allow_marketing_email",
            field=models.BooleanField(
                default=True,
                verbose_name="Minulle saa l\xe4hett\xe4\xe4 tapahtumaan liittyvi\xe4 tiedotteita s\xe4hk\xf6postitse",
            ),
        ),
    ]
