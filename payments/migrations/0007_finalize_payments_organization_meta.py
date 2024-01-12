# Generated by Django 2.2.10 on 2020-07-21 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0006_populate_payments_organization_meta"),
    ]

    operations = [
        migrations.AlterField(
            model_name="checkoutpayment",
            name="event",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="core.Event"
            ),
        ),
        migrations.AlterField(
            model_name="checkoutpayment",
            name="organization",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.Organization"),
        ),
    ]
