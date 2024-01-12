from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0013_auto_20151219_1510"),
    ]

    operations = [
        migrations.AddField(
            model_name="term",
            name="payment_type",
            field=models.CharField(
                default="bank_transfer",
                max_length=13,
                verbose_name="Maksutapa",
                choices=[("bank_transfer", "Tilisiirto")],
            ),
        ),
    ]
