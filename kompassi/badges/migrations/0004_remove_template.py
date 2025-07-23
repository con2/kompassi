from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("badges", "0003_populate_personnel_class"),
    ]

    operations = [
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
