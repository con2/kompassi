# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_organization_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='logo_url',
            field=models.CharField(default=b'', help_text='Voi olla paikallinen (alkaa /-merkill\xe4) tai absoluuttinen (alkaa http/https)', max_length=255, verbose_name='Organisaation logon URL', blank=True),
            preserve_default=True,
        ),
    ]
