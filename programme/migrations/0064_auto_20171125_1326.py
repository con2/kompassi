# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-25 11:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0063_remove_view_rooms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['event', 'name'], 'verbose_name': 'Room', 'verbose_name_plural': 'Rooms'},
        ),
        migrations.RemoveField(
            model_name='room',
            name='order',
        ),
    ]