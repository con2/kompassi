# Generated by Django 4.2.9 on 2024-01-07 06:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("program_v2", "0008_alter_dimension_title_alter_dimensionvalue_title"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0039_alter_person_birth_date_alter_person_email_and_more"),
        ("forms", "0015_rename_globalformresponse_response_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="EventForm",
            new_name="Form",
        ),
        migrations.DeleteModel(
            name="GlobalForm",
        ),
    ]
