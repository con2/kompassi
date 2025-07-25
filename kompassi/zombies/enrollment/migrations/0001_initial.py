# Generated by Django 1.9.9 on 2016-10-11 17:02


import django.db.models.deletion
from django.db import migrations, models

import kompassi.core.models.group_management_mixin


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0023_auto_20160704_2155"),
        ("auth", "0007_alter_validators_add_error_messages"),
    ]

    operations = [
        migrations.CreateModel(
            name="Enrollment",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "special_diet_other",
                    models.TextField(
                        blank=True,
                        help_text="If you're on a diet that's not included in the list, please detail your diet here. Event organizer will try to take dietary needs into consideration, but all diets may not be catered for.",
                        verbose_name="Other diets",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EnrollmentEventMeta",
            fields=[
                (
                    "event",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="enrollmenteventmeta",
                        serialize=False,
                        to="core.Event",
                    ),
                ),
                (
                    "form_class_path",
                    models.CharField(
                        help_text="Reference to form class. Example: events.yukicon2016.forms:EnrollmentForm",
                        max_length=63,
                    ),
                ),
                ("enrollment_opens", models.DateTimeField(blank=True, null=True, verbose_name="Enrollment opens")),
                ("enrollment_closes", models.DateTimeField(blank=True, null=True, verbose_name="Enrollment closes")),
                ("admin_group", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="auth.Group")),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, kompassi.core.models.group_management_mixin.GroupManagementMixin),
        ),
        migrations.CreateModel(
            name="SpecialDiet",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=63)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="enrollment",
            name="event",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.Event"),
        ),
        migrations.AddField(
            model_name="enrollment",
            name="person",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.Person"),
        ),
        migrations.AddField(
            model_name="enrollment",
            name="special_diet",
            field=models.ManyToManyField(blank=True, to="enrollment.SpecialDiet", verbose_name="Diet"),
        ),
    ]
