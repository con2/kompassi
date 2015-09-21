# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('desuprofile_integration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmationcode',
            name='next_url',
            field=models.CharField(default=b'', max_length=1023, blank=True),
            preserve_default=True,
        ),
    ]
