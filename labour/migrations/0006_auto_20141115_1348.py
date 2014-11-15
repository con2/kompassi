# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labour', '0005_jobcategory_app_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workperiod',
            name='end_time',
            field=models.DateTimeField(null=True, verbose_name='Loppuaika', blank=True),
        ),
        migrations.AlterField(
            model_name='workperiod',
            name='start_time',
            field=models.DateTimeField(null=True, verbose_name='Alkuaika', blank=True),
        ),
    ]
