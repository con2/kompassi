import django.db.models.deletion
import django_enum.fields
from django.db import migrations, models


def populate_involvement_app_and_type(apps, schema_editor):
    Involvement = apps.get_model("involvement", "Involvement")

    bulk_update = []
    for involvement in Involvement.objects.all():
        involvement.app = involvement.cached_dimensions["app"][0]
        involvement.type = involvement.cached_dimensions["type"][0]
        bulk_update.append(involvement)
    Involvement.objects.bulk_update(bulk_update, ["app", "type"], batch_size=400)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0043_emailverificationtoken_language_and_more"),
        ("dimensions", "0014_alter_dimension_can_values_be_added"),
        ("forms", "0053_surveydefaultinvolvementdimensionvalue"),
        ("involvement", "0005_alter_involvement_universe_involvementtobadgemapping_and_more"),
        ("program_v2", "0045_programv2eventmeta_konsti_url_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="InvolvementEventMeta",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ],
        ),
        migrations.AddField(
            model_name="involvement",
            name="annotations",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="involvement",
            name="app",
            field=django_enum.fields.EnumCharField(
                choices=[
                    ("forms", "FORMS"),
                    ("program", "PROGRAM"),
                    ("involvement", "INVOLVEMENT"),
                    ("volunteers", "VOLUNTEERS"),
                ],
                default="",
                max_length=11,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="involvement",
            name="type",
            field=django_enum.fields.EnumCharField(
                choices=[
                    ("program-offer", "PROGRAM_OFFER"),
                    ("program-host", "PROGRAM_HOST"),
                    ("survey-response", "SURVEY_RESPONSE"),
                    ("combined-perks", "COMBINED_PERKS"),
                    ("legacy-signup", "LEGACY_SIGNUP"),
                ],
                default="",
                max_length=15,
            ),
            preserve_default=False,
        ),
        migrations.RunPython(
            populate_involvement_app_and_type,
            migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.AddIndex(
            model_name="involvement",
            index=models.Index(
                fields=["universe", "person", "app", "type"],
                name="involvement_univers_1342ca_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="involvement",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    (
                        "app__in",
                        [
                            "forms",
                            "program",
                            "involvement",
                            "volunteers",
                        ],
                    )
                ),
                name="involvement_Involvement_app_InvolvementApp",
            ),
        ),
        migrations.AddConstraint(
            model_name="involvement",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    (
                        "type__in",
                        [
                            "program-offer",
                            "program-host",
                            "survey-response",
                            "combined-perks",
                            "legacy-signup",
                        ],
                    )
                ),
                name="involvement_Involvement_type_InvolvementType",
            ),
        ),
        migrations.AddField(
            model_name="involvementeventmeta",
            name="default_registry",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="involvement.registry",
            ),
        ),
        migrations.AddField(
            model_name="involvementeventmeta",
            name="event",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="core.event",
            ),
        ),
        migrations.AddField(
            model_name="involvementeventmeta",
            name="universe",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, related_name="+", to="dimensions.universe"
            ),
        ),
    ]
