from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [  # noqa: RUF012
        ("core", "0006_organization_description"),
    ]

    operations = [  # noqa: RUF012
        migrations.AddField(
            model_name="organization",
            name="logo_url",
            field=models.CharField(
                default="",
                help_text="Voi olla paikallinen (alkaa /-merkill\xe4) tai absoluuttinen (alkaa http/https)",
                max_length=255,
                verbose_name="Organisaation logon URL",
                blank=True,
            ),
            preserve_default=True,
        ),
    ]
