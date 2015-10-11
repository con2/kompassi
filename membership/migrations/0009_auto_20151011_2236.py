# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0008_auto_20151011_2229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membershipfeepayment',
            options={'verbose_name': 'J\xe4senmaksusuoritus', 'verbose_name_plural': 'J\xe4senmaksusuoritukset'},
        ),
    ]
