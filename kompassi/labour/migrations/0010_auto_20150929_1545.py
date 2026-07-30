from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("labour", "0009_remove_signup_work_periods"),
    ]

    operations = [  # noqa: RUF012
        migrations.AlterField(
            model_name="jobrequirement",
            name="job",
            field=models.ForeignKey(
                on_delete=models.CASCADE, related_name="requirements", verbose_name="teht\xe4v\xe4", to="labour.Job"
            ),
            preserve_default=True,
        ),
    ]
