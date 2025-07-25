# Generated by Django 2.2.10 on 2020-07-21 17:08

import django.db.models.deletion
from django.db import migrations, models

import kompassi.core.models.group_management_mixin


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0034_event_cancelled"),
        ("payments", "0004_checkout_v2"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentsOrganizationMeta",
            fields=[
                (
                    "organization",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="core.Organization",
                    ),
                ),
                ("checkout_password", models.CharField(max_length=255)),
                ("checkout_merchant", models.CharField(max_length=255)),
            ],
            bases=(models.Model, kompassi.core.models.group_management_mixin.GroupManagementMixin),
        ),
        migrations.AlterModelOptions(
            name="paymentseventmeta",
            options={},
        ),
        migrations.AddField(
            model_name="checkoutpayment",
            name="organization",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="core.Organization"
            ),
        ),
    ]
