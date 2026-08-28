import django_enum.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("dimensions", "0018_rename_program_v2_app_value_to_program"),
    ]

    operations = [  # noqa: RUF012
        migrations.RenameField(
            model_name="universe",
            old_name="app_name",
            new_name="app",
        ),
        migrations.AlterField(
            model_name="universe",
            name="app",
            field=django_enum.fields.EnumCharField(
                choices=[
                    ("forms", "FORMS"),
                    ("program", "PROGRAM"),
                    ("involvement", "INVOLVEMENT"),
                    ("volunteers", "VOLUNTEERS"),
                ],
                max_length=11,
            ),
        ),
        migrations.AddConstraint(
            model_name="universe",
            constraint=models.CheckConstraint(
                condition=models.Q(("app__in", ["forms", "program", "involvement", "volunteers"])),
                name="dimensions_Universe_app_DimensionApp",
            ),
        ),
    ]
