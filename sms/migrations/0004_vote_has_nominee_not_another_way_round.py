# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0003_refactoring'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nominee',
            name='vote',
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote',
            field=models.ForeignKey(to='sms.Nominee'),
            preserve_default=True,
        ),
    ]
