import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailVerificationToken",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("code", models.CharField(unique=True, max_length=63)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("used_at", models.DateTimeField(null=True, blank=True)),
                (
                    "state",
                    models.CharField(
                        default="valid",
                        max_length=8,
                        choices=[("valid", "Kelvollinen"), ("used", "K\xe4ytetty"), ("revoked", "Mit\xe4t\xf6ity")],
                    ),
                ),
                ("email", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Event",
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
                ("name", models.CharField(max_length=63, verbose_name="Tapahtuman nimi")),
                ("headline", models.CharField(default="", max_length=63, verbose_name="Alaotsikko", blank=True)),
                (
                    "name_genitive",
                    models.CharField(
                        help_text="Esimerkki: Susiconin", max_length=63, verbose_name="Tapahtuman nimi genetiiviss\xe4"
                    ),
                ),
                (
                    "name_illative",
                    models.CharField(
                        help_text="Esimerkki: Susiconiin", max_length=63, verbose_name="Tapahtuman nimi illatiiviss\xe4"
                    ),
                ),
                (
                    "name_inessive",
                    models.CharField(
                        help_text="Esimerkki: Susiconissa",
                        max_length=63,
                        verbose_name="Tapahtuman nimi inessiiviss\xe4",
                    ),
                ),
                ("description", models.TextField(verbose_name="Kuvaus", blank=True)),
                ("start_time", models.DateTimeField(null=True, verbose_name="Alkamisaika", blank=True)),
                ("end_time", models.DateTimeField(null=True, verbose_name="P\xe4\xe4ttymisaika", blank=True)),
                ("homepage_url", models.CharField(max_length=255, verbose_name="Tapahtuman kotisivu", blank=True)),
                (
                    "organization_name",
                    models.CharField(max_length=63, verbose_name="J\xe4rjest\xe4v\xe4 taho", blank=True),
                ),
                (
                    "organization_url",
                    models.CharField(max_length=255, verbose_name="J\xe4rjest\xe4v\xe4n tahon kotisivu", blank=True),
                ),
                (
                    "public",
                    models.BooleanField(
                        default=True,
                        help_text="Julkiset tapahtumat n\xe4ytet\xe4\xe4n etusivulla.",
                        verbose_name="Julkinen",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tapahtuma",
                "verbose_name_plural": "Tapahtumat",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="PasswordResetToken",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("code", models.CharField(unique=True, max_length=63)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("used_at", models.DateTimeField(null=True, blank=True)),
                (
                    "state",
                    models.CharField(
                        default="valid",
                        max_length=8,
                        choices=[("valid", "Kelvollinen"), ("used", "K\xe4ytetty"), ("revoked", "Mit\xe4t\xf6ity")],
                    ),
                ),
                ("ip_address", models.CharField(max_length=45, blank=True)),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("first_name", models.CharField(max_length=1023, verbose_name="Etunimi")),
                ("surname", models.CharField(max_length=1023, verbose_name="Sukunimi")),
                ("nick", models.CharField(help_text="Lempi- tai kutsumanimi", max_length=1023, blank=True)),
                (
                    "birth_date",
                    models.DateField(
                        help_text="Syntym\xe4aika muodossa 24.2.1994",
                        null=True,
                        verbose_name="Syntym\xe4aika",
                        blank=True,
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="S\xe4hk\xf6posti on ensisijainen yhteydenpitokeino tapahtumaan liittyviss\xe4 asioissa.",
                        max_length=255,
                        verbose_name="S\xe4hk\xf6postiosoite",
                        blank=True,
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        help_text="Puhelinnumeroasi k\xe4ytet\xe4\xe4n tarvittaessa kiireellisiin yhteydenottoihin koskien osallistumistasi tapahtumaan.",
                        max_length=255,
                        verbose_name="Puhelinnumero",
                        blank=True,
                    ),
                ),
                (
                    "may_send_info",
                    models.BooleanField(
                        default=False,
                        verbose_name="Minulle saa l\xe4hett\xe4\xe4 s\xe4hk\xf6postitse tietoa tulevista tapahtumista <i>(vapaaehtoinen)</i>",
                    ),
                ),
                (
                    "preferred_name_display_style",
                    models.CharField(
                        blank=True,
                        help_text="T\xe4ss\xe4 voit vaikuttaa siihen, miss\xe4 muodossa nimesi esitet\xe4\xe4n (esim. painetaan badgeesi).",
                        max_length=31,
                        verbose_name="Nimen esitt\xe4minen",
                        choices=[
                            ("firstname_nick_surname", 'Etunimi "Nick" Sukunimi'),
                            ("firstname_surname", "Etunimi Sukunimi"),
                            ("firstname", "Etunimi"),
                            ("nick", "Nick"),
                        ],
                    ),
                ),
                ("notes", models.TextField(verbose_name="K\xe4sittelij\xe4n merkinn\xe4t", blank=True)),
                ("email_verified_at", models.DateTimeField(null=True, blank=True)),
                (
                    "user",
                    models.OneToOneField(on_delete=models.CASCADE, null=True, blank=True, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "ordering": ["surname"],
                "verbose_name": "Henkil\xf6",
                "verbose_name_plural": "Henkil\xf6t",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Venue",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=63, verbose_name="Tapahtumapaikan nimi")),
                (
                    "name_inessive",
                    models.CharField(
                        help_text="Esimerkki: Paasitornissa",
                        max_length=63,
                        verbose_name="Tapahtumapaikan nimi inessiiviss\xe4",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tapahtumapaikka",
                "verbose_name_plural": "Tapahtumapaikat",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="passwordresettoken",
            name="person",
            field=models.ForeignKey(on_delete=models.CASCADE, to="core.Person"),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name="passwordresettoken",
            index_together={("person", "state")},
        ),
        migrations.AddField(
            model_name="event",
            name="venue",
            field=models.ForeignKey(on_delete=models.CASCADE, verbose_name="Tapahtumapaikka", to="core.Venue"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="emailverificationtoken",
            name="person",
            field=models.ForeignKey(on_delete=models.CASCADE, to="core.Person"),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name="emailverificationtoken",
            index_together={("person", "state")},
        ),
    ]
