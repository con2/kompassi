from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("desuprofile_integration", "0002_confirmationcode_next_url"),
    ]

    operations = [  # noqa: RUF012
        migrations.AddField(
            model_name="confirmationcode",
            name="desuprofile_username",
            field=models.CharField(max_length=30, verbose_name="Desuprofiilin k\xe4ytt\xe4j\xe4nimi", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="connection",
            name="desuprofile_username",
            field=models.CharField(max_length=30, verbose_name="Desuprofiilin k\xe4ytt\xe4j\xe4nimi", blank=True),
            preserve_default=True,
        ),
    ]
