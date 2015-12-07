# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labour', '0015_shift'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shift',
            options={'ordering': ('job', 'start_time'), 'verbose_name': 'ty\xf6vuoro', 'verbose_name_plural': 'ty\xf6vuorot'},
        ),
    ]
