# Generated by Django 2.2.16 on 2020-10-25 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0034_event_cancelled"),
        ("labour", "0033_auto_20170802_1500"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArchivedSignup",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("job_title", models.CharField(blank=True, default="", max_length=63, verbose_name="Tehtävänimike")),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="archived_signups", to="core.Event"
                    ),
                ),
                (
                    "job_categories_accepted",
                    models.ManyToManyField(
                        blank=True,
                        related_name="archived_signups",
                        to="labour.JobCategory",
                        verbose_name="Hyväksytyt tehtäväalueet",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="archived_signups", to="core.Person"
                    ),
                ),
                (
                    "personnel_classes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="archived_signups",
                        to="labour.PersonnelClass",
                        verbose_name="Henkilöstöluokat",
                    ),
                ),
            ],
        ),
    ]
