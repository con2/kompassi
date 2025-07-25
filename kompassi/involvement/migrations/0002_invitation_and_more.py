# Generated by Django 5.1.5 on 2025-05-17 17:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import kompassi.event_log_v2.utils.monthly_partitions
import kompassi.tickets_v2.optimized_server.utils.uuid7


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0043_emailverificationtoken_language_and_more"),
        ("dimensions", "0010_alter_universe_app"),
        ("forms", "0042_survey_purpose_slug_alter_survey_anonymity"),
        ("involvement", "0001_initial"),
        ("program_v2", "0039_programv2eventmeta_default_registry"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Invitation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=kompassi.tickets_v2.optimized_server.utils.uuid7.uuid7,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("used_at", models.DateTimeField(blank=True, null=True)),
                (
                    "language",
                    models.CharField(
                        choices=[("en", "English"), ("fi", "Finnish"), ("sv", "Swedish")],
                        default="en",
                        help_text="The language of the invitation. This is used to send the invitation in the correct language.",
                        max_length=2,
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="The email address of the person to invite. This is used to send the invitation.",
                        max_length=255,
                    ),
                ),
            ],
            bases=(kompassi.event_log_v2.utils.monthly_partitions.UUID7Mixin, models.Model),
        ),
        migrations.RemoveIndex(
            model_name="involvement",
            name="involvement_univers_eeb99e_idx",
        ),
        migrations.RemoveIndex(
            model_name="involvement",
            name="involvement_program_idx",
        ),
        migrations.RemoveIndex(
            model_name="involvement",
            name="involvement_response_idx",
        ),
        migrations.RemoveField(
            model_name="involvement",
            name="app_name",
        ),
        migrations.AlterField(
            model_name="involvement",
            name="universe",
            field=models.ForeignKey(
                db_index=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="involvements",
                to="dimensions.universe",
            ),
        ),
        migrations.AddField(
            model_name="invitation",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="invitations_created",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="invitation",
            name="program",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="invitations",
                to="program_v2.program",
            ),
        ),
        migrations.AddField(
            model_name="invitation",
            name="survey",
            field=models.ForeignKey(
                help_text="When a user accepts this invitation, they will fill in this survey.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="invitations",
                to="forms.survey",
            ),
        ),
        migrations.AddField(
            model_name="involvement",
            name="invitation",
            field=models.ForeignKey(
                blank=True,
                db_index=False,
                help_text="Invitation that was used to create this involvement, if any.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="involvements",
                to="involvement.invitation",
            ),
        ),
        migrations.AddIndex(
            model_name="involvement",
            index=models.Index(
                fields=["universe", "person", "program", "response"], name="involvement_univers_c36687_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="involvement",
            index=models.Index(
                condition=models.Q(("program__isnull", False)), fields=["program"], name="involvement_program_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="involvement",
            index=models.Index(
                condition=models.Q(("response__isnull", False)), fields=["response"], name="involvement_response_idx"
            ),
        ),
    ]
