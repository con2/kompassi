from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("labour", "0012_auto_20151017_0012"),
    ]

    operations = [  # noqa: RUF012
        migrations.AddField(
            model_name="signup",
            name="time_confirmation_requested",
            field=models.DateTimeField(null=True, verbose_name="Vahvistusta vaadittu", blank=True),
            preserve_default=True,
        ),
    ]
