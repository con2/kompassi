from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("labour", "0005_jobcategory_app_label"),
    ]

    operations = [  # noqa: RUF012
        migrations.AlterField(
            model_name="workperiod",
            name="end_time",
            field=models.DateTimeField(null=True, verbose_name="Loppuaika", blank=True),
        ),
        migrations.AlterField(
            model_name="workperiod",
            name="start_time",
            field=models.DateTimeField(null=True, verbose_name="Alkuaika", blank=True),
        ),
    ]
