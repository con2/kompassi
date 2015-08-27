# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='grantedprivilege',
            name='state',
            field=models.CharField(default=b'granted', max_length=8, choices=[(b'pending', 'Odottaa hyv\xe4ksynt\xe4\xe4'), (b'approved', 'Hyv\xe4ksytty, odottaa toteutusta'), (b'granted', 'My\xf6nnetty'), (b'rejected', 'Hyl\xe4tty')]),
            preserve_default=True,
        ),
    ]
