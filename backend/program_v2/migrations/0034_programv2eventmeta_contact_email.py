# Generated by Django 5.1.5 on 2025-04-19 14:00

import re

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("program_v2", "0033_program_program_offer_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="programv2eventmeta",
            name="contact_email",
            field=models.CharField(
                blank=True,
                help_text="Foo Bar <foo.bar@example.com>",
                max_length=255,
                validators=[django.core.validators.RegexValidator(re.compile("(?P<name>.+) <(?P<email>.+@.+\\..+)>"))],
            ),
        ),
    ]
