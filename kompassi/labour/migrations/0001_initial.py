import django.core.validators
from django.db import migrations, models

import kompassi.core.csv_export


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0001_initial"),
        ("contenttypes", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AlternativeSignupForm",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "slug",
                    models.CharField(
                        help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.',
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
                (
                    "title",
                    models.CharField(
                        help_text="T\xe4m\xe4 otsikko n\xe4kyy k\xe4ytt\xe4j\xe4lle.",
                        max_length=63,
                        verbose_name="Otsikko",
                    ),
                ),
                (
                    "signup_form_class_path",
                    models.CharField(
                        help_text="Viittaus ilmoittautumislomakkeen toteuttavaan luokkaan. Esimerkki: tracon9.forms:ConcomSignupForm",
                        max_length=63,
                    ),
                ),
                (
                    "signup_extra_form_class_path",
                    models.CharField(
                        default="labour.forms:EmptySignupExtraForm",
                        help_text="Viittaus lis\xe4tietolomakkeen toteuttavaan luokkaan. Esimerkki: tracon9.forms:ConcomSignupExtraForm",
                        max_length=63,
                    ),
                ),
                ("active_from", models.DateTimeField(null=True, verbose_name="K\xe4ytt\xf6aika alkaa", blank=True)),
                (
                    "active_until",
                    models.DateTimeField(null=True, verbose_name="K\xe4ytt\xf6aika p\xe4\xe4ttyy", blank=True),
                ),
                (
                    "signup_message",
                    models.TextField(
                        default="",
                        help_text="T\xe4m\xe4 viesti n\xe4ytet\xe4\xe4n kaikille t\xe4t\xe4 lomaketta k\xe4ytt\xe4ville ty\xf6voimailmoittautumisen alussa. K\xe4ytettiin esimerkiksi Tracon 9:ss\xe4 kertomaan, ett\xe4 ty\xf6voimahaku on avoinna en\xe4\xe4 JV:ille ja erikoisteht\xe4ville.",
                        null=True,
                        verbose_name="Ilmoittautumisen huomautusviesti",
                        blank=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Vaihtoehtoinen ilmoittautumislomake",
                "verbose_name_plural": "Vaihtoehtoiset ilmoittautumislomakkeet",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="InfoLink",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "url",
                    models.CharField(
                        help_text="Muista aloittaa ulkoiset linkit <i>http://</i> tai <i>https://</i>.",
                        max_length=255,
                        verbose_name="Osoite",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Teksti")),
            ],
            options={
                "verbose_name": "ty\xf6voimaohje",
                "verbose_name_plural": "ty\xf6voimaohjeet",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("title", models.CharField(max_length=63, verbose_name="teht\xe4v\xe4n nimi")),
            ],
            options={
                "verbose_name": "teht\xe4v\xe4",
                "verbose_name_plural": "teht\xe4v\xe4t",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="JobCategory",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=63, verbose_name="teht\xe4v\xe4alueen nimi")),
                (
                    "slug",
                    models.CharField(
                        help_text='Tekninen nimi eli "slug" n\xe4kyy URL-osoitteissa. Sallittuja merkkej\xe4 ovat pienet kirjaimet, numerot ja v\xe4liviiva. Teknist\xe4 nime\xe4 ei voi muuttaa luomisen j\xe4lkeen.',
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
                (
                    "description",
                    models.TextField(
                        help_text="Kuvaus n\xe4kyy hakijoille hakulomakkeella. Kerro ainakin, mik\xe4li teht\xe4v\xe4\xe4n tarvitaan erityisi\xe4 tietoja tai taitoja.",
                        verbose_name="teht\xe4v\xe4alueen kuvaus",
                        blank=True,
                    ),
                ),
                (
                    "public",
                    models.BooleanField(
                        default=True,
                        help_text="Teht\xe4viin, jotka eiv\xe4t ole avoimessa haussa, voi hakea vain ty\xf6voimavastaavan l\xe4hett\xe4m\xe4ll\xe4 hakulinkill\xe4.",
                        verbose_name="avoimessa haussa",
                    ),
                ),
            ],
            options={
                "verbose_name": "teht\xe4v\xe4alue",
                "verbose_name_plural": "teht\xe4v\xe4alueet",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="JobRequirement",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "count",
                    models.IntegerField(
                        default=0,
                        verbose_name="vaadittu henkil\xf6m\xe4\xe4r\xe4",
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("start_time", models.DateTimeField(verbose_name="vaatimuksen alkuaika")),
                ("end_time", models.DateTimeField(verbose_name="vaatimuksen p\xe4\xe4ttymisaika")),
                ("job", models.ForeignKey(on_delete=models.CASCADE, verbose_name="teht\xe4v\xe4", to="labour.Job")),
            ],
            options={
                "verbose_name": "henkil\xf6st\xf6vaatimus",
                "verbose_name_plural": "henkil\xf6st\xf6vaatimukset",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="LabourEventMeta",
            fields=[
                (
                    "event",
                    models.OneToOneField(
                        on_delete=models.CASCADE,
                        related_name="laboureventmeta",
                        primary_key=True,
                        serialize=False,
                        to="core.Event",
                    ),
                ),
                (
                    "registration_opens",
                    models.DateTimeField(null=True, verbose_name="ty\xf6voimahaku alkaa", blank=True),
                ),
                (
                    "registration_closes",
                    models.DateTimeField(null=True, verbose_name="ty\xf6voimahaku p\xe4\xe4ttyy", blank=True),
                ),
                ("work_begins", models.DateTimeField(verbose_name="Ensimm\xe4iset ty\xf6vuorot alkavat")),
                ("work_ends", models.DateTimeField(verbose_name="Viimeiset ty\xf6vuorot p\xe4\xe4ttyv\xe4t")),
                (
                    "monitor_email",
                    models.CharField(
                        help_text="Kaikki ty\xf6voimaj\xe4rjestelm\xe4n l\xe4hett\xe4m\xe4t s\xe4hk\xf6postiviestit l\xe4hetet\xe4\xe4n my\xf6s t\xe4h\xe4n osoitteeseen.",
                        max_length=255,
                        verbose_name="tarkkailus\xe4hk\xf6posti",
                        blank=True,
                    ),
                ),
                (
                    "contact_email",
                    models.CharField(
                        help_text="Kaikki ty\xf6voimaj\xe4rjestelm\xe4n l\xe4hett\xe4m\xe4t s\xe4hk\xf6postiviestit l\xe4hetet\xe4\xe4n t\xe4st\xe4 osoitteesta, ja t\xe4m\xe4 osoite n\xe4ytet\xe4\xe4n ty\xf6voimalle yhteysosoitteena. Muoto: Selite &lt;osoite@esimerkki.fi&gt;.",
                        max_length=255,
                        verbose_name="yhteysosoite",
                        blank=True,
                    ),
                ),
                (
                    "signup_message",
                    models.TextField(
                        default="",
                        help_text="T\xe4m\xe4 viesti n\xe4ytet\xe4\xe4n kaikille ty\xf6voimailmoittautumisen alussa. K\xe4ytettiin esimerkiksi Tracon 9:ss\xe4 kertomaan, ett\xe4 ty\xf6voimahaku on avoinna en\xe4\xe4 JV:ille ja erikoisteht\xe4ville.",
                        null=True,
                        verbose_name="Ilmoittautumisen huomautusviesti",
                        blank=True,
                    ),
                ),
                ("admin_group", models.ForeignKey(on_delete=models.CASCADE, to="auth.Group")),
                (
                    "signup_extra_content_type",
                    models.ForeignKey(on_delete=models.CASCADE, to="contenttypes.ContentType"),
                ),
            ],
            options={
                "verbose_name": "tapahtuman ty\xf6voimatiedot",
                "verbose_name_plural": "tapahtuman ty\xf6voimatiedot",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="PersonQualification",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("person", models.ForeignKey(on_delete=models.CASCADE, verbose_name="henkil\xf6", to="core.Person")),
            ],
            options={
                "verbose_name": "p\xe4tevyyden haltija",
                "verbose_name_plural": "p\xe4tevyyden haltijat",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Qualification",
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
                ("name", models.CharField(max_length=63, verbose_name="p\xe4tevyyden nimi")),
                ("description", models.TextField(verbose_name="kuvaus", blank=True)),
                (
                    "qualification_extra_content_type",
                    models.ForeignKey(on_delete=models.CASCADE, blank=True, to="contenttypes.ContentType", null=True),
                ),
            ],
            options={
                "verbose_name": "p\xe4tevyys",
                "verbose_name_plural": "p\xe4tevyydet",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Signup",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "notes",
                    models.TextField(
                        help_text="T\xe4m\xe4 kentt\xe4 ei normaalisti n\xe4y henkil\xf6lle itselleen, mutta jos t\xe4m\xe4 pyyt\xe4\xe4 henkil\xf6rekisteriotetta, kent\xe4n arvo on siihen sis\xe4llytett\xe4v\xe4.",
                        verbose_name="K\xe4sittelij\xe4n merkinn\xe4t",
                        blank=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Luotu")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="P\xe4ivitetty")),
                (
                    "xxx_interim_shifts",
                    models.TextField(
                        default="",
                        help_text="T\xe4m\xe4 tekstikentt\xe4 on v\xe4liaikaisratkaisu, jolla v\xe4nk\xe4rin ty\xf6vuorot voidaan merkit\xe4 Kompassiin ja l\xe4hett\xe4\xe4 v\xe4nk\xe4rille ty\xf6voimaviestiss\xe4 jo ennen kuin lopullinen ty\xf6vuoroty\xf6kalu on k\xe4ytt\xf6kunnossa.",
                        null=True,
                        verbose_name="Ty\xf6vuorot",
                        blank=True,
                    ),
                ),
                (
                    "job_title",
                    models.CharField(
                        default="",
                        help_text="Printataan badgeen ym. Asetetaan automaattisesti hyv\xe4ksyttyjen teht\xe4v\xe4alueiden perusteella, mik\xe4li kentt\xe4 j\xe4tet\xe4\xe4n tyhj\xe4ksi.",
                        max_length=63,
                        verbose_name="Teht\xe4v\xe4nimike",
                        blank=True,
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Aktiivinen")),
                ("time_accepted", models.DateTimeField(null=True, verbose_name="Hyv\xe4ksytty", blank=True)),
                ("time_finished", models.DateTimeField(null=True, verbose_name="Vuorot valmiit", blank=True)),
                ("time_complained", models.DateTimeField(null=True, verbose_name="Vuoroista reklamoitu", blank=True)),
                ("time_cancelled", models.DateTimeField(null=True, verbose_name="Peruutettu", blank=True)),
                ("time_rejected", models.DateTimeField(null=True, verbose_name="Hyl\xe4tty", blank=True)),
                ("time_arrived", models.DateTimeField(null=True, verbose_name="Saapunut tapahtumaan", blank=True)),
                (
                    "time_work_accepted",
                    models.DateTimeField(null=True, verbose_name="Ty\xf6panos hyv\xe4ksytty", blank=True),
                ),
                (
                    "time_reprimanded",
                    models.DateTimeField(null=True, verbose_name="Ty\xf6panoksesta esitetty moite", blank=True),
                ),
            ],
            options={
                "verbose_name": "ilmoittautuminen",
                "verbose_name_plural": "ilmoittautumiset",
            },
            bases=(models.Model, kompassi.core.csv_export.CsvExportMixin),
        ),
        migrations.CreateModel(
            name="EmptySignupExtra",
            fields=[
                (
                    "signup",
                    models.OneToOneField(
                        on_delete=models.CASCADE,
                        related_name="+",
                        primary_key=True,
                        serialize=False,
                        to="labour.Signup",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="WorkPeriod",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("description", models.CharField(max_length=63, verbose_name="Kuvaus")),
                ("start_time", models.DateTimeField(verbose_name="Alkuaika")),
                ("end_time", models.DateTimeField(verbose_name="Loppuaika")),
                ("event", models.ForeignKey(on_delete=models.CASCADE, verbose_name="Tapahtuma", to="core.Event")),
            ],
            options={
                "verbose_name": "ty\xf6vuorotoive",
                "verbose_name_plural": "ty\xf6vuorotoiveet",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="signup",
            name="alternative_signup_form_used",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                blank=True,
                to="labour.AlternativeSignupForm",
                help_text="T\xe4m\xe4 kentt\xe4 ilmaisee, mit\xe4 ilmoittautumislomaketta hakemuksen t\xe4ytt\xe4miseen k\xe4ytettiin. Jos kentt\xe4 on tyhj\xe4, k\xe4ytettiin oletuslomaketta.",
                null=True,
                verbose_name="Ilmoittautumislomake",
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="signup",
            name="event",
            field=models.ForeignKey(on_delete=models.CASCADE, to="core.Event"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="signup",
            name="job_categories",
            field=models.ManyToManyField(
                help_text="Valitse kaikki ne teht\xe4v\xe4t, joissa olisit valmis ty\xf6skentelem\xe4\xe4n tapahtumassa. Huomaathan, ett\xe4 sinulle tarjottavia teht\xe4vi\xe4 voi rajoittaa se, mit\xe4 p\xe4tevyyksi\xe4 olet ilmoittanut sinulla olevan. Esimerkiksi j\xe4rjestyksenvalvojaksi voivat ilmoittautua ainoastaan JV-kortilliset.",
                related_name="signup_set",
                verbose_name="Haettavat teht\xe4v\xe4t",
                to="labour.JobCategory",
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="signup",
            name="job_categories_accepted",
            field=models.ManyToManyField(
                related_name="accepted_signup_set",
                to="labour.JobCategory",
                blank=True,
                help_text="Teht\xe4v\xe4alueet, joilla hyv\xe4ksytty vapaaehtoisty\xf6ntekij\xe4 tulee ty\xf6skentelem\xe4\xe4n. T\xe4m\xe4n perusteella henkil\xf6lle mm. l\xe4hetet\xe4\xe4n oman teht\xe4v\xe4alueensa ty\xf6voimaohjeet. Harmaalla merkityt teht\xe4v\xe4alueet ovat niit\xe4, joihin hakija ei ole itse hakenut.",
                null=True,
                verbose_name="Hyv\xe4ksytyt teht\xe4v\xe4alueet",
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="signup",
            name="person",
            field=models.ForeignKey(on_delete=models.CASCADE, to="core.Person"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="signup",
            name="work_periods",
            field=models.ManyToManyField(
                help_text="Valitse kaikki ne ajanjaksot, joina voit ty\xf6skennell\xe4 tapahtumassa. T\xe4m\xe4 ei ole lopullinen ty\xf6vuorosi, vaan ty\xf6voimatiimi pyrkii sijoittamaan ty\xf6vuorosi n\xe4ille ajoille.",
                related_name="signup_set",
                verbose_name="Ty\xf6vuorotoiveet",
                to="labour.WorkPeriod",
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="personqualification",
            name="qualification",
            field=models.ForeignKey(on_delete=models.CASCADE, verbose_name="p\xe4tevyys", to="labour.Qualification"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="jobcategory",
            name="event",
            field=models.ForeignKey(on_delete=models.CASCADE, verbose_name="tapahtuma", to="core.Event"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="jobcategory",
            name="required_qualifications",
            field=models.ManyToManyField(to="labour.Qualification", verbose_name="vaaditut p\xe4tevyydet", blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name="jobcategory",
            unique_together={("event", "slug")},
        ),
        migrations.AddField(
            model_name="job",
            name="job_category",
            field=models.ForeignKey(
                on_delete=models.CASCADE, verbose_name="teht\xe4v\xe4alue", to="labour.JobCategory"
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="infolink",
            name="event",
            field=models.ForeignKey(on_delete=models.CASCADE, verbose_name="Tapahtuma", to="core.Event"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="infolink",
            name="group",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                verbose_name="Ryhm\xe4",
                to="auth.Group",
                help_text="Linkki n\xe4ytet\xe4\xe4n vain t\xe4m\xe4n ryhm\xe4n j\xe4senille.",
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="alternativesignupform",
            name="event",
            field=models.ForeignKey(on_delete=models.CASCADE, verbose_name="Tapahtuma", to="core.Event"),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name="alternativesignupform",
            unique_together={("event", "slug")},
        ),
    ]
