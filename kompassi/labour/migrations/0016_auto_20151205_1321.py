from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("labour", "0015_shift"),
    ]

    operations = [  # noqa: RUF012
        migrations.AlterModelOptions(
            name="shift",
            options={
                "ordering": ("job", "start_time"),
                "verbose_name": "ty\xf6vuoro",
                "verbose_name_plural": "ty\xf6vuorot",
            },
        ),
    ]
