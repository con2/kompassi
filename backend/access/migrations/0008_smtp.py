from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_person_allow_work_history_sharing"),
        ("access", "0007_accessorganizationmeta"),
    ]

    operations = [
        migrations.CreateModel(
            name="SMTPPassword",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("password_hash", models.CharField(max_length=255, verbose_name="Salasanan tarkiste")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Luotu")),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name="smtp_passwords",
                        verbose_name="Henkil\xf6",
                        to="core.Person",
                    ),
                ),
            ],
            options={
                "verbose_name": "SMTP-salasana",
                "verbose_name_plural": "SMTP-salasanat",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="SMTPServer",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("hostname", models.CharField(max_length=255, verbose_name="SMTP-palvelin")),
                (
                    "domains",
                    models.ManyToManyField(
                        related_name="smtp_servers", verbose_name="Verkkotunnukset", to="access.EmailAliasDomain"
                    ),
                ),
            ],
            options={
                "verbose_name": "SMTP-palvelin",
                "verbose_name_plural": "SMTP-palvelimet",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="smtppassword",
            name="smtp_server",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name="smtp_passwords",
                verbose_name="SMTP-palvelin",
                to="access.SMTPServer",
            ),
            preserve_default=True,
        ),
    ]
