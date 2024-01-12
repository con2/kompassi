from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mailings", "0002_message_channel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="subject_template",
            field=models.CharField(
                help_text="HUOM! Otsikko n\xe4kyy vastaanottajalle ainoastaan, jos viesti l\xe4hetet\xe4\xe4n s\xe4hk\xf6postitse. Tekstiviestill\xe4 l\xe4hetett\xe4ville viesteille otsikkoa k\xe4ytet\xe4\xe4n ainoastaan viestin tunnistamiseen sis\xe4isesti.",
                max_length=255,
                verbose_name="Otsikko",
            ),
            preserve_default=True,
        ),
    ]
