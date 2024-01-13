from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labour", "0008_auto_20150419_1438"),
        ("badges", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="badge",
            name="personnel_class",
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to="labour.PersonnelClass", null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="batch",
            name="personnel_class",
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to="labour.PersonnelClass", null=True),
            preserve_default=True,
        ),
    ]
