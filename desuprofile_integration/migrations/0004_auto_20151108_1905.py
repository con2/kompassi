# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('desuprofile_integration', '0003_auto_20151016_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='user',
            field=models.OneToOneField(verbose_name='K\xe4ytt\xe4j\xe4', to=settings.AUTH_USER_MODEL),
        ),
    ]
