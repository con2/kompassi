from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("membership", "0012_members_group"),
    ]

    operations = [  # noqa: RUF012
        migrations.AlterField(
            model_name="membership",
            name="state",
            field=models.CharField(
                max_length=10,
                verbose_name="Tila",
                choices=[
                    ("approval", "Odottaa hyv\xe4ksynt\xe4\xe4"),
                    ("in_effect", "Voimassa"),
                    ("discharged", "Erotettu"),
                    ("declined", "Hyl\xe4tty"),
                ],
            ),
        ),
    ]
