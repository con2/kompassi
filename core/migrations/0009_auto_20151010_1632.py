# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_person_muncipality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='muncipality',
            field=models.CharField(help_text='Virallinen kotikuntasi eli kunta jossa olet kirjoilla.', max_length=127, verbose_name='Kotikunta', blank=True),
            preserve_default=True,
        ),
    ]
