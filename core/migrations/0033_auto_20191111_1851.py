# Generated by Django 2.1.12 on 2019-11-11 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_event_timestamps'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='badge_name_display_style',
            new_name='preferred_badge_name_display_style',
        ),
    ]