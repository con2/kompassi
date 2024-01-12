from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labour", "0006_auto_20141115_1348"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobcategory",
            name="personnel_classes",
            field=models.ManyToManyField(to="labour.PersonnelClass", verbose_name="yhteiskuntaluokat", blank=True),
            preserve_default=True,
        ),
    ]
