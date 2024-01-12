# Generated by Django 2.2.17 on 2021-02-17 17:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0100_programme_hitpoint2020_preferred_time_slots"),
    ]

    operations = [
        migrations.AddField(
            model_name="programme",
            name="ropecon2021_gamedesk_physical_or_virtual",
            field=models.CharField(
                choices=[
                    ("phys_only", "I can organize my programme only at a physical con"),
                    ("virt_only", "I can organize my programme only at a virtual con"),
                    ("phys_or_virt", "I can organize my programme both at a physical con and at a virtual con"),
                ],
                default="phys_only",
                help_text="The organizers of Ropecon strive to organize a physical con, and if the con can be held thusly, virtual programmes will not be organized. If the con cannot be face to face, we cannot organize physical programmes during a virtual con.<br><br>Specify here whether your programme can be organized face to face, virtually, or either way.",
                max_length=12,
                null=True,
                verbose_name="Physical or virtual programme?",
            ),
        ),
    ]
