from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("labour", "0011_job_slug"),
    ]

    operations = [  # noqa: RUF012
        migrations.AlterField(
            model_name="jobcategory",
            name="personnel_classes",
            field=models.ManyToManyField(to="labour.PersonnelClass", verbose_name="Henkil\xf6st\xf6luokat", blank=True),
            preserve_default=True,
        ),
    ]
