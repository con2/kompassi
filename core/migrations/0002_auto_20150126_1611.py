# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='logo_url',
            field=models.CharField(default=b'', help_text='Voi olla paikallinen (alkaa /-merkill\xe4) tai absoluuttinen (alkaa http/https)', max_length=255, verbose_name='Tapahtuman logon URL', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(default=b'', help_text='Muutaman kappaleen mittainen kuvaus tapahtumasta. N\xe4kyy tapahtumasivulla.', verbose_name='Tapahtuman kuvaus', blank=True),
        ),
    ]
