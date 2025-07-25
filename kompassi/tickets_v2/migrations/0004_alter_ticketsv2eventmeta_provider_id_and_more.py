# Generated by Django 5.1.5 on 2025-04-09 06:40

from django.db import migrations, models

import kompassi.tickets_v2.optimized_server.models.enums


class Migration(migrations.Migration):
    dependencies = [
        ("tickets_v2", "0003_ticketsv2eventmeta_terms_and_conditions_url_en_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticketsv2eventmeta",
            name="provider_id",
            field=models.SmallIntegerField(
                choices=[(0, "NONE"), (1, "PAYTRAIL"), (2, "STRIPE")],
                default=kompassi.tickets_v2.optimized_server.models.enums.PaymentProvider["NONE"],
                verbose_name="Payment provider",
            ),
        ),
        migrations.AlterField(
            model_name="ticketsv2eventmeta",
            name="terms_and_conditions_url_en",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="ticketsv2eventmeta",
            name="terms_and_conditions_url_fi",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="ticketsv2eventmeta",
            name="terms_and_conditions_url_sv",
            field=models.TextField(blank=True, default=""),
        ),
    ]
