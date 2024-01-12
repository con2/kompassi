# Generated by Django 1.10.8 on 2018-02-12 20:18
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ropecon2018", "0001_initial"),
        ("programme", "0065_auto_20171227_0037"),
    ]

    operations = [
        migrations.AddField(
            model_name="programme",
            name="ropecon2018_preferred_time_slots",
            field=models.ManyToManyField(
                help_text="When would you like to run your RPG? The time slots are intentionally vague. If you have more specific needs regarding the time, please explain them in the last open field.",
                to="ropecon2018.TimeSlot",
                verbose_name="preferred time slots",
            ),
        ),
    ]
