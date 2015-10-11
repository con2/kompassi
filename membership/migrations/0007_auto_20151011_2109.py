# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0006_auto_20151011_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='state',
            field=models.CharField(max_length=10, verbose_name='Tila', choices=[('approval', 'Odottaa hyv\xe4ksynt\xe4\xe4'), ('in_effect', 'Voimassa'), ('discharged', 'Erotettu')]),
            preserve_default=True,
        ),
    ]
