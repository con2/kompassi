# Generated by Django 2.2.10 on 2020-07-23 17:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0007_finalize_payments_organization_meta"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="checkoutpayment",
            options={"ordering": ("-created_at",)},
        ),
    ]