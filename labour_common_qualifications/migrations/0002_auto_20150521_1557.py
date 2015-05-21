# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('labour_common_qualifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jvkortti',
            name='card_number',
            field=models.CharField(help_text='Muoto: 0000/J0000/00 tai XX/0000/00', max_length=b'13', verbose_name='JV-kortin numero', validators=[django.core.validators.RegexValidator(regex=b'.+/.+/.+', message='Tarkista JV-kortin numero')]),
            preserve_default=True,
        ),
    ]
