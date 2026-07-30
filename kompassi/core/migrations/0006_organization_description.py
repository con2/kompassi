from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("core", "0005_auto_20151008_2225"),
    ]

    operations = [  # noqa: RUF012
        migrations.AddField(
            model_name="organization",
            name="description",
            field=models.TextField(verbose_name="Kuvaus", blank=True),
            preserve_default=True,
        ),
    ]
