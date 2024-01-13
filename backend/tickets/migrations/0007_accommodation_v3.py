from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0006_ticketseventmeta_receipt_footer"),
    ]

    operations = [
        migrations.CreateModel(
            name="AccommodationInformation",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("first_name", models.CharField(default="", max_length=100, verbose_name="Etunimi", blank=True)),
                ("last_name", models.CharField(default="", max_length=100, verbose_name="Sukunimi", blank=True)),
                ("phone_number", models.CharField(default="", max_length=30, verbose_name="Puhelinnumero", blank=True)),
                (
                    "email",
                    models.EmailField(
                        default="", max_length=75, verbose_name="S\xc3\xa4hk\xc3\xb6postiosoite", blank=True
                    ),
                ),
                (
                    "order_product",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name="accommodation_information_set",
                        to="tickets.OrderProduct",
                    ),
                ),
            ],
            options={
                "verbose_name": "majoittujan tiedot",
                "verbose_name_plural": "majoittujan tiedot",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="product",
            name="requires_accommodation_information",
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
