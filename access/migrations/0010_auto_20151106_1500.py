# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0009_privilege_disclaimers'),
    ]

    operations = [
        migrations.AddField(
            model_name='smtpserver',
            name='crypto',
            field=models.CharField(default=b'tls', max_length=5, verbose_name='Salaus', choices=[(b'plain', b'Ei salausta'), (b'ssl', b'SSL'), (b'tls', b'TLS')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='smtpserver',
            name='port',
            field=models.IntegerField(default=587, verbose_name='Porttinumero'),
            preserve_default=True,
        ),
    ]
