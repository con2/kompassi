from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("core", "0001_initial"),
    ]

    operations = [  # noqa: RUF012
        migrations.AddField(
            model_name="event",
            name="logo_url",
            field=models.CharField(
                default="",
                help_text="Voi olla paikallinen (alkaa /-merkill\xe4) tai absoluuttinen (alkaa http/https)",
                max_length=255,
                verbose_name="Tapahtuman logon URL",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="event",
            name="description",
            field=models.TextField(
                default="",
                help_text="Muutaman kappaleen mittainen kuvaus tapahtumasta. N\xe4kyy tapahtumasivulla.",
                verbose_name="Tapahtuman kuvaus",
                blank=True,
            ),
        ),
    ]
