# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-02-12 21:26
from __future__ import unicode_literals

from django.db import migrations

from core.utils import slugify


def populate_slug(apps, schema_editor):
    Tag = apps.get_model('programme', 'tag')

    for tag in Tag.objects.all():
        tag.slug = slugify(tag.title)
        tag.save()


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0052_tag_slug'),
    ]

    operations = [
        migrations.RunPython(populate_slug)
    ]
