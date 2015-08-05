# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_personnel_class(apps, schema_editor):
    Badge = apps.get_model('badges', 'Badge')
    PersonnelClass = apps.get_model('labour', 'PersonnelClass')

    for badge in Badge.objects.all():
        if badge.personnel_class is None:
            badge.personnel_class, unused = PersonnelClass.objects.get_or_create(
                event=badge.template.event,
                slug=badge.template.slug,
                defaults=dict(
                    name=badge.template.name,
                    app_label='labour',
                )
            )
            badge.save()


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0002_batch_personnel_class'),
    ]

    operations = [
        migrations.RunPython(populate_personnel_class),
    ]
