from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("labour", "0008_auto_20150419_1438"),
    ]

    operations = [  # noqa: RUF012
        migrations.RemoveField(
            model_name="signup",
            name="work_periods",
        ),
    ]
