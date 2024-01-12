# Generated by Django 2.1.5 on 2019-03-01 21:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0087_auto_20190301_2337"),
    ]

    operations = [
        migrations.AlterField(
            model_name="programme",
            name="max_players",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="What is the maximum number of players that can take part in a single run of the game?",
                null=True,
                validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)],
                verbose_name="maximum number of players",
            ),
        ),
    ]
