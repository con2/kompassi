from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("access", "0009_privilege_disclaimers"),
    ]

    operations = [
        migrations.AddField(
            model_name="smtpserver",
            name="crypto",
            field=models.CharField(
                default="tls",
                max_length=5,
                verbose_name="Salaus",
                choices=[("plain", "Ei salausta"), ("ssl", "SSL"), ("tls", "TLS")],
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="smtpserver",
            name="port",
            field=models.IntegerField(default=587, verbose_name="Porttinumero"),
            preserve_default=True,
        ),
    ]
