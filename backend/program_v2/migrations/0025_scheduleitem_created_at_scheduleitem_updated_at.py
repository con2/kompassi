# Generated by Django 5.0.9 on 2024-10-27 10:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("program_v2", "0024_remove_program_favorited_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="scheduleitem",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="scheduleitem",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
