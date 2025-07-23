from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labour", "0004_auto_20141115_1337"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobcategory",
            name="app_label",
            field=models.CharField(default="labour", max_length=63, blank=True),
            preserve_default=True,
        ),
    ]
