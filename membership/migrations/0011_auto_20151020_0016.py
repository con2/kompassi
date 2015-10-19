# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0010_remove_membershiporganizationmeta_membership_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='organization',
            field=models.ForeignKey(related_name='memberships', verbose_name='Yhdistys', to='core.Organization'),
            preserve_default=True,
        ),
    ]
