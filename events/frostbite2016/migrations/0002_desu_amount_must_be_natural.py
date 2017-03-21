# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


# was thinking about 0xDEADBEEF but "Values from -2147483648 to 2147483647 are safe in all databases supported by Django." :(
MARKER_VALUE = 0xC0FFEE


def fix_negative_desu_amounts(apps, schema_editor):
    SignupExtra = apps.get_model('frostbite2016', 'signupextra')
    SignupExtra.objects.filter(desu_amount__lt=0).update(desu_amount=MARKER_VALUE)


class Migration(migrations.Migration):

    dependencies = [
        ('frostbite2016', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fix_negative_desu_amounts, elidable=True),
        migrations.AlterField(
            model_name='signupextra',
            name='desu_amount',
            field=models.PositiveIntegerField(help_text='Kuinka monessa Desuconissa olet ollut v\xe4nk\xe4rin\xe4?', verbose_name='Desum\xe4\xe4r\xe4'),
            preserve_default=True,
        ),
    ]
