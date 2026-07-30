from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("access", "0008_smtp"),
    ]

    operations = [  # noqa: RUF012
        migrations.AddField(
            model_name="privilege",
            name="disclaimers",
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
