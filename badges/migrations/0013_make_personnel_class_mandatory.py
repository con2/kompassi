# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-29 20:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0012_delete_spurious_badges'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='personnel_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labour.PersonnelClass', verbose_name='Personnel class'),
        ),
    ]
