from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("badges", "0003_populate_personnel_class"),
    ]

    operations = [  # noqa: RUF012
        migrations.RemoveField(
            model_name="badge",
            name="template",
        ),
        migrations.RemoveField(
            model_name="batch",
            name="template",
        ),
        migrations.DeleteModel(
            name="Template",
        ),
    ]
