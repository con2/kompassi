# Generated by Django 5.0.10 on 2024-12-16 13:33

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tickets_v2", "0002_product_max_per_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="etickets_per_product",
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
