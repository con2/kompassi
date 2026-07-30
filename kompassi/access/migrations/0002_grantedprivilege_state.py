from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("access", "0001_initial"),
    ]

    operations = [  # noqa: RUF012
        migrations.AddField(
            model_name="grantedprivilege",
            name="state",
            field=models.CharField(
                default="granted",
                max_length=8,
                choices=[
                    ("pending", "Odottaa hyv\xe4ksynt\xe4\xe4"),
                    ("approved", "Hyv\xe4ksytty, odottaa toteutusta"),
                    ("granted", "My\xf6nnetty"),
                    ("rejected", "Hyl\xe4tty"),
                ],
            ),
            preserve_default=True,
        ),
    ]
