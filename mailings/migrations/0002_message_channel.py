# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='channel',
            field=models.CharField(default='email', max_length=5, verbose_name='Kanava', choices=[(b'email', b'S\xc3\xa4hk\xc3\xb6posti'), (b'sms', b'Tekstiviesti')]),
            preserve_default=True,
        ),
    ]
