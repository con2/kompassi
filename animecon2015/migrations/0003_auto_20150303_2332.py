# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animecon2015', '0002_remove_signupextra_construction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupextra',
            name='total_work',
            field=models.CharField(verbose_name='Toivottu kokonaisty\xf6m\xe4\xe4r\xe4', max_length=15, choices=[('10h', b'10 tuntia'), ('12h', b'12 tuntia'), ('yli12h', b'Yli 12 tuntia')], help_text='Kuinka paljon haluat tehd\xe4 t\xf6it\xe4 yhteens\xe4 tapahtuman aikana? Useimmissa teht\xe4vist\xe4 minimi on kahdeksan tuntia, mutta joissain teht\xe4viss\xe4 se voi olla my\xf6s v\xe4hemm\xe4n (esim. majoitusvalvonta 6 h).'),
        ),
    ]
