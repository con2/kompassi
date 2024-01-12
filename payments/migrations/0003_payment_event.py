from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
        ("payments", "0002_paymentseventmeta"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="event",
            field=models.ForeignKey(on_delete=models.CASCADE, default=1, to="core.Event"),
            preserve_default=False,
        ),
    ]
