# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hitpoint2015', '0002_auto_20150930_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupextra',
            name='overseer',
            field=models.BooleanField(default=False, help_text='Vuorovastaavat ovat kokeneempia conity\xf6l\xe4isi\xe4, jotka toimivat oman teht\xe4v\xe4alueensa tiiminvet\xe4j\xe4n\xe4.', verbose_name='Olen kiinnostunut vuorovastaavan teht\xe4vist\xe4'),
            preserve_default=True,
        ),
    ]
