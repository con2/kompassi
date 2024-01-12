from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0001_initial"),
        ("core", "0016_person_allow_work_history_sharing"),
        ("access", "0004_descriptions"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailAlias",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "account_name",
                    models.CharField(
                        help_text="Ennen @-merkki\xe4 tuleva osa s\xe4hk\xf6postiosoitetta. Muodostetaan automaattisesti jos tyhj\xe4.",
                        max_length=255,
                        verbose_name="Tunnus",
                        blank=True,
                    ),
                ),
                (
                    "email_address",
                    models.CharField(
                        help_text="Muodostetaan automaattisesti", max_length=511, verbose_name="S\xe4hk\xf6postiosoite"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Luotu")),
                ("modified_at", models.DateTimeField(auto_now=True, verbose_name="Muokattu")),
            ],
            options={
                "verbose_name": "S\xe4hk\xf6postialias",
                "verbose_name_plural": "S\xe4hk\xf6postialiakset",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="EmailAliasDomain",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "domain_name",
                    models.CharField(
                        help_text="Esim. example.com", unique=True, max_length=255, verbose_name="Verkkotunnus"
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=models.CASCADE, verbose_name="Organisaatio", to="core.Organization"),
                ),
            ],
            options={
                "verbose_name": "Verkkotunnus",
                "verbose_name_plural": "Verkkotunnukset",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="EmailAliasType",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "metavar",
                    models.CharField(
                        default="etunimi.sukunimi",
                        help_text='Esim. "etunimi.sukunimi"',
                        max_length=255,
                        verbose_name="Metamuuttuja",
                    ),
                ),
                (
                    "account_name_code",
                    models.CharField(default="access.email_aliases:firstname_surname", max_length=255),
                ),
                (
                    "domain",
                    models.ForeignKey(
                        on_delete=models.CASCADE, verbose_name="Verkkotunnus", to="access.EmailAliasDomain"
                    ),
                ),
            ],
            options={
                "verbose_name": "S\xe4hk\xf6postialiaksen tyyppi",
                "verbose_name_plural": "S\xe4hk\xf6postialiasten tyypit",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="GroupEmailAliasGrant",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("group", models.ForeignKey(on_delete=models.CASCADE, verbose_name="Ryhm\xe4", to="auth.Group")),
                (
                    "type",
                    models.ForeignKey(on_delete=models.CASCADE, verbose_name="Tyyppi", to="access.EmailAliasType"),
                ),
            ],
            options={
                "verbose_name": "My\xf6nt\xe4miskanava",
                "verbose_name_plural": "My\xf6nt\xe4miskanavat",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="emailalias",
            name="domain",
            field=models.ForeignKey(
                on_delete=models.CASCADE, verbose_name="Verkkotunnus", to="access.EmailAliasDomain"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="emailalias",
            name="group_grant",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                blank=True,
                to="access.GroupEmailAliasGrant",
                help_text="My\xf6nt\xe4miskanava antaa kaikille tietyn ryhm\xe4n j\xe4senille tietyntyyppisen s\xe4hk\xf6postialiaksen. Jos aliakselle on asetettu my\xf6nt\xe4miskanava, alias on my\xf6nnetty t\xe4m\xe4n my\xf6nt\xe4miskanavan perusteella, ja kun my\xf6nt\xe4miskanava vanhenee, kaikki sen perusteella my\xf6nnetyt aliakset voidaan poistaa kerralla.",
                null=True,
                verbose_name="My\xf6nt\xe4miskanava",
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="emailalias",
            name="person",
            field=models.ForeignKey(
                on_delete=models.CASCADE, related_name="email_aliases", verbose_name="Henkil\xf6", to="core.Person"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="emailalias",
            name="type",
            field=models.ForeignKey(on_delete=models.CASCADE, verbose_name="Tyyppi", to="access.EmailAliasType"),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name="emailalias",
            unique_together={("domain", "account_name")},
        ),
    ]
