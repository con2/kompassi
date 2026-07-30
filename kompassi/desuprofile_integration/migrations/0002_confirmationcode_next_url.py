from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("desuprofile_integration", "0001_initial"),
    ]

    operations = [  # noqa: RUF012
        migrations.AddField(
            model_name="confirmationcode",
            name="next_url",
            field=models.CharField(default="", max_length=1023, blank=True),
            preserve_default=True,
        ),
    ]
