from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("mailings", "0001_initial"),
    ]

    operations = [  # noqa: RUF012
        migrations.AddField(
            model_name="message",
            name="channel",
            field=models.CharField(
                default="email",
                max_length=5,
                verbose_name="Kanava",
                choices=[("email", "S\xc3\xa4hk\xc3\xb6posti"), ("sms", "Tekstiviesti")],
            ),
            preserve_default=True,
        ),
    ]
