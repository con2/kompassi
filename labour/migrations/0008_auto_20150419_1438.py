# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labour', '0007_jobcategory_personnel_classes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='personnel_classes',
            field=models.ManyToManyField(help_text='Mihin henkil\xf6st\xf6ryhmiin t\xe4m\xe4 henkil\xf6 kuuluu? Henkil\xf6 saa valituista ryhmist\xe4 ylimm\xe4n mukaisen badgen.', to='labour.PersonnelClass', verbose_name='Yhteiskuntaluokat', blank=True),
            preserve_default=True,
        ),
    ]
