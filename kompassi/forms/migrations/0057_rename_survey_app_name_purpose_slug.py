import django_enum.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("core", "0044_organization_business_id"),
        ("dimensions", "0019_rename_universe_app_name_to_app"),
        ("forms", "0056_rename_program_v2_app_value_to_program"),
        ("involvement", "0010_involvementeventmeta_admin_group"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [  # noqa: RUF012
        migrations.RenameField(
            model_name="survey",
            old_name="app_name",
            new_name="app",
        ),
        migrations.RenameField(
            model_name="survey",
            old_name="purpose_slug",
            new_name="purpose",
        ),
        migrations.AlterField(
            model_name="survey",
            name="app",
            field=django_enum.fields.EnumCharField(
                choices=[
                    ("forms", "FORMS"),
                    ("program", "PROGRAM"),
                    ("involvement", "INVOLVEMENT"),
                    ("volunteers", "VOLUNTEERS"),
                ],
                default="forms",
                help_text="Which app manages this survey?",
                max_length=11,
            ),
        ),
        migrations.AlterField(
            model_name="survey",
            name="purpose",
            field=django_enum.fields.EnumCharField(
                choices=[
                    ("DEFAULT", "DEFAULT"),
                    ("INVITE", "INVITE"),
                ],
                default="DEFAULT",
                help_text=(
                    "Generic surveys and program offers are DEFAULT, program host invitations are ACCEPT_INVITATION."
                ),
                max_length=7,
            ),
        ),
        migrations.AddConstraint(
            model_name="survey",
            constraint=models.CheckConstraint(
                condition=models.Q(("app__in", ["forms", "program", "involvement", "volunteers"])),
                name="forms_Survey_app_DimensionApp",
            ),
        ),
        migrations.AddConstraint(
            model_name="survey",
            constraint=models.CheckConstraint(
                condition=models.Q(("purpose__in", ["DEFAULT", "INVITE"])),
                name="forms_Survey_purpose_SurveyPurpose",
            ),
        ),
    ]
