# Generated by Django 1.9.1 on 2016-01-27 16:12


from django.db import migrations
import programme.proxies.helpers


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0016_freeformorganizer"),
    ]

    operations = [
        migrations.CreateModel(
            name="FreeformOrganizerAdminProxy",
            fields=[],
            options={
                "verbose_name": "freeform organizer",
                "proxy": True,
                "verbose_name_plural": "freeform organizers",
            },
            bases=("programme.freeformorganizer", programme.proxies.helpers.ProgrammeyThingamajieAdminHelperMixin),
        ),
    ]
