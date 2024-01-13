from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0005_auto_20150208_1455"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticketseventmeta",
            name="receipt_footer",
            field=models.CharField(
                default="",
                help_text="T\xe4m\xe4 teksti tulostetaan postitettavien tilausten pakkauslistan alatunnisteeseen. T\xe4ss\xe4 on hyv\xe4 mainita mm. j\xe4rjest\xe4v\xe4n tahon yhteystiedot.",
                max_length=1023,
                verbose_name="Pakkauslistan alatunniste",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
