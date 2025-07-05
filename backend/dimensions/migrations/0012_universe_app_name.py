from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dimensions", "0011_dimensionvalue_is_subject_locked"),
    ]

    operations = [
        migrations.RenameField(
            model_name="universe",
            old_name="app",
            new_name="app_name",
        ),
        migrations.AlterField(
            model_name="universe",
            name="app_name",
            field=models.CharField(
                choices=[
                    ("forms", "FORMS"),
                    ("program_v2", "PROGRAM_V2"),
                    ("involvement", "INVOLVEMENT"),
                ],
                max_length=11,
            ),
        ),
    ]
