# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_person_allow_work_history_sharing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='headline',
        ),
    ]
