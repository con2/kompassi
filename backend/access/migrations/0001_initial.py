import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0001_initial"),
        ("core", "0003_auto_20150813_1907"),
    ]

    operations = [
        migrations.CreateModel(
            name="GrantedPrivilege",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("granted_at", models.DateTimeField(auto_now_add=True)),
                (
                    "person",
                    models.ForeignKey(on_delete=models.CASCADE, related_name="granted_privileges", to="core.Person"),
                ),
            ],
            options={
                "verbose_name": "My\xf6nnetty k\xe4ytt\xf6oikeus",
                "verbose_name_plural": "My\xf6nnetyt k\xe4ytt\xf6oikeudet",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="GroupPrivilege",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name="group_privileges",
                        blank=True,
                        to="core.Event",
                        null=True,
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(on_delete=models.CASCADE, related_name="group_privileges", to="auth.Group"),
                ),
            ],
            options={
                "verbose_name": "Ryhm\xe4n k\xe4ytt\xf6oikeus",
                "verbose_name_plural": "Ryhmien k\xe4ytt\xf6oikeudet",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Privilege",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "slug",
                    models.CharField(
                        help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.',
                        unique=True,
                        max_length=63,
                        verbose_name="Tekninen nimi",
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="[a-z0-9-]+",
                                message="Tekninen nimi saa sis\xe4lt\xe4\xe4 vain pieni\xe4 kirjaimia, numeroita sek\xe4 v\xe4liviivoja.",
                            )
                        ],
                    ),
                ),
                ("title", models.CharField(max_length=256)),
                ("description", models.TextField(blank=True)),
                ("request_success_message", models.TextField(blank=True)),
                ("grant_code", models.CharField(max_length=256)),
            ],
            options={
                "verbose_name": "K\xe4ytt\xf6oikeus",
                "verbose_name_plural": "K\xe4ytt\xf6oikeudet",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="groupprivilege",
            name="privilege",
            field=models.ForeignKey(on_delete=models.CASCADE, related_name="group_privileges", to="access.Privilege"),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name="groupprivilege",
            unique_together={("privilege", "group")},
        ),
        migrations.AddField(
            model_name="grantedprivilege",
            name="privilege",
            field=models.ForeignKey(on_delete=models.CASCADE, related_name="granted_privileges", to="access.Privilege"),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name="grantedprivilege",
            unique_together={("privilege", "person")},
        ),
    ]
