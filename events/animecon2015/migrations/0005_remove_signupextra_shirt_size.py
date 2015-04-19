# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animecon2015', '0004_signupextra_personal_identification_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signupextra',
            name='shirt_size',
        ),
    ]
