# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-28 23:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desucon2016', '0003_auto_20160128_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupextra',
            name='free_text',
            field=models.TextField(blank=True, help_text='Jos haluat sanoa hakemuksesi k\xe4sittelij\xf6ille jotain sellaista, jolle ei ole omaa kentt\xe4\xe4 yll\xe4, k\xe4yt\xe4 t\xe4t\xe4 kentt\xe4\xe4. Jos haet valokuvaajaksi, kerro lis\xe4ksi millaista kuvauskalustoa sinulla on k\xe4ytett\xe4viss\xe4si ja listaamuutamia gallerialinkkej\xe4, joista p\xe4\xe4semme ihailemaan ottamiasi kuvia. ', verbose_name='Vapaa alue'),
        ),
    ]