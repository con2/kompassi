from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("core", "0001_initial"),
        ("payments", "0002_paymentseventmeta"),
    ]

    operations = [  # noqa: RUF012
        migrations.AddField(
            model_name="payment",
            name="event",
            field=models.ForeignKey(on_delete=models.CASCADE, default=1, to="core.Event"),
            preserve_default=False,
        ),
    ]
