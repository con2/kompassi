from django.db import migrations, models

import kompassi.core.csv_export
import kompassi.zombies.programme.models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("title", models.CharField(max_length=1023)),
                ("style", models.CharField(max_length=15)),
                ("notes", models.TextField(blank=True)),
                ("public", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["title"],
                "verbose_name": "ohjelmaluokka",
                "verbose_name_plural": "ohjelmaluokat",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Programme",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "title",
                    models.CharField(
                        help_text="Keksi ohjelmanumerollesi lyhyt ja ytimek\xe4s otsikko ohjelmakarttaa sek\xe4 ohjelmalehte\xe4 varten. Tracon varaa oikeuden muuttaa otsikkoa.",
                        max_length=1023,
                        verbose_name="Otsikko",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Ohjelmakuvaus n\xe4kyy web-ohjelmakartassa sek\xe4 ohjelmalehdess\xe4. Ohjelmakuvauksen tarkoitus on antaa k\xe4vij\xe4lle riitt\xe4v\xe4t tiedot p\xe4\xe4tt\xe4\xe4, osallistuako ohjelmaasi, ja markkinoida ohjelmaasi k\xe4vij\xf6ille. Tracon varaa oikeuden editoida kuvausta.",
                        verbose_name="Ohjelmanumeron kuvaus",
                        blank=True,
                    ),
                ),
                (
                    "room_requirements",
                    models.TextField(
                        help_text="Kuinka paljon odotat ohjelmanumerosi vet\xe4v\xe4n yleis\xf6\xe4? Mink\xe4laista salia toivot ohjelmanumerosi k\xe4ytt\xf6\xf6n?",
                        verbose_name="Tilatarpeet",
                        blank=True,
                    ),
                ),
                (
                    "tech_requirements",
                    models.TextField(
                        help_text="Tarvitsetko ohjelmasi pit\xe4miseen esimerkiksi tietokonetta, videotykki\xe4, luento\xe4\xe4nentoistoa, musiikki\xe4\xe4nentoistoa, tussi-, fl\xe4ppi- tai liitutaulua tai muita erityisv\xe4lineit\xe4? Oman tietokoneen k\xe4ytt\xf6 on mahdollista vain, jos siit\xe4 on sovittu etuk\xe4teen.",
                        verbose_name="Tekniikkatarpeet",
                        blank=True,
                    ),
                ),
                (
                    "requested_time_slot",
                    models.TextField(
                        help_text="Mihin aikaan haluaisit pit\xe4\xe4 ohjelmanumerosi? Mink\xe4 ohjelmanumeroiden kanssa et halua olla p\xe4\xe4llek\xe4in?",
                        verbose_name="Aikatoiveet",
                        blank=True,
                    ),
                ),
                (
                    "video_permission",
                    models.CharField(
                        default="public",
                        help_text="Saako luentosi videoida ja julkaista Internetiss\xe4?",
                        max_length=15,
                        verbose_name="Videointilupa",
                        choices=[
                            ("public", "Ohjelmanumeroni saa videoida ja julkaista"),
                            (
                                "private",
                                "Kiell\xe4n ohjelmanumeroni julkaisun, mutta sen saa videoida arkistok\xe4ytt\xf6\xf6n",
                            ),
                            ("forbidden", "Kiell\xe4n ohjelmanumeroni videoinnin"),
                        ],
                    ),
                ),
                (
                    "notes_from_host",
                    models.TextField(
                        help_text="Jos haluat sanoa ohjelmanumeroosi liittyen jotain, mik\xe4 ei sovi mihink\xe4\xe4n yll\xe4 olevista kentist\xe4, k\xe4yt\xe4 t\xe4t\xe4 kentt\xe4\xe4.",
                        verbose_name="Vapaamuotoiset terveiset ohjelmavastaaville",
                        blank=True,
                    ),
                ),
                ("start_time", models.DateTimeField(null=True, verbose_name="Alkuaika", blank=True)),
                (
                    "length",
                    models.IntegerField(
                        help_text="Ohjelmalla tulee olla tila, alkuaika ja kesto, jotta se n\xe4kyisi ohjelmakartassa.",
                        null=True,
                        verbose_name="Kesto (minuuttia)",
                        blank=True,
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        help_text="T\xe4m\xe4 kentt\xe4 ei normaalisti n\xe4y ohjelman j\xe4rjest\xe4j\xe4lle, mutta jos henkil\xf6 pyyt\xe4\xe4 henkil\xf6rekisteriotetta, kent\xe4n arvo on siihen sis\xe4llytett\xe4v\xe4.",
                        verbose_name="Ohjelmavastaavan muistiinpanot",
                        blank=True,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(on_delete=models.CASCADE, verbose_name="Ohjelmaluokka", to="programme.Category"),
                ),
            ],
            options={
                "ordering": ["start_time", "room"],
                "verbose_name": "ohjelmanumero",
                "verbose_name_plural": "ohjelmanumerot",
            },
            bases=(models.Model, kompassi.core.csv_export.CsvExportMixin),
        ),
        migrations.CreateModel(
            name="ProgrammeEditToken",
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
                ("person", models.ForeignKey(on_delete=models.CASCADE, to="core.Person")),
                ("programme", models.ForeignKey(on_delete=models.CASCADE, to="programme.Programme")),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ProgrammeEventMeta",
            fields=[
                (
                    "event",
                    models.OneToOneField(
                        on_delete=models.CASCADE,
                        related_name="programmeeventmeta",
                        primary_key=True,
                        serialize=False,
                        to="core.Event",
                    ),
                ),
                ("public", models.BooleanField(default=True)),
                (
                    "contact_email",
                    models.CharField(
                        help_text="Kaikki ohjelmaj\xe4rjestelm\xe4n l\xe4hett\xe4m\xe4t s\xe4hk\xf6postiviestit l\xe4hetet\xe4\xe4n t\xe4st\xe4 osoitteesta, ja t\xe4m\xe4 osoite n\xe4ytet\xe4\xe4n ohjelmanj\xe4rjest\xe4j\xe4lle yhteysosoitteena. Muoto: Selite &lt;osoite@esimerkki.fi&gt;.",
                        max_length=255,
                        verbose_name="yhteysosoite",
                        blank=True,
                    ),
                ),
                ("admin_group", models.ForeignKey(on_delete=models.CASCADE, to="auth.Group")),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ProgrammeRole",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("person", models.ForeignKey(on_delete=models.CASCADE, to="core.Person")),
                ("programme", models.ForeignKey(on_delete=models.CASCADE, to="programme.Programme")),
            ],
            options={
                "verbose_name": "ohjelmanpit\xe4j\xe4n rooli",
                "verbose_name_plural": "ohjelmanpit\xe4jien roolit",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("title", models.CharField(max_length=1023)),
                ("require_contact_info", models.BooleanField(default=True)),
                ("is_default", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["title"],
                "verbose_name": "rooli",
                "verbose_name_plural": "roolit",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=1023)),
                ("order", models.IntegerField()),
                ("public", models.BooleanField(default=True)),
                ("notes", models.TextField(blank=True)),
                ("venue", models.ForeignKey(on_delete=models.CASCADE, to="core.Venue")),
            ],
            options={
                "ordering": ["venue", "order"],
                "verbose_name": "tila",
                "verbose_name_plural": "tilat",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="SpecialStartTime",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("start_time", models.DateTimeField(verbose_name="alkuaika")),
                ("event", models.ForeignKey(on_delete=models.CASCADE, verbose_name="tapahtuma", to="core.Event")),
            ],
            options={
                "ordering": ["event", "start_time"],
                "verbose_name": "poikkeava alkuaika",
                "verbose_name_plural": "poikkeavat alkuajat",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("title", models.CharField(max_length=15)),
                ("order", models.IntegerField(default=0)),
                ("style", models.CharField(default="label-default", max_length=15)),
                ("event", models.ForeignKey(on_delete=models.CASCADE, to="core.Event")),
            ],
            options={
                "ordering": ["order"],
                "verbose_name": "t\xe4gi",
                "verbose_name_plural": "t\xe4git",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="TimeBlock",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("event", models.ForeignKey(on_delete=models.CASCADE, to="core.Event")),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="View",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=32)),
                ("public", models.BooleanField(default=True)),
                ("order", models.IntegerField(default=0)),
                ("event", models.ForeignKey(on_delete=models.CASCADE, to="core.Event")),
                ("rooms", models.ManyToManyField(to="programme.Room")),
            ],
            options={
                "ordering": ["event", "order"],
                "verbose_name": "ohjelmakarttan\xe4kym\xe4",
                "verbose_name_plural": "ohjelmakarttan\xe4kym\xe4t",
            },
            bases=(models.Model, kompassi.zombies.programme.models.ViewMethodsMixin),
        ),
        migrations.AlterUniqueTogether(
            name="specialstarttime",
            unique_together={("event", "start_time")},
        ),
        migrations.AlterUniqueTogether(
            name="room",
            unique_together={("venue", "order")},
        ),
        migrations.AddField(
            model_name="programmerole",
            name="role",
            field=models.ForeignKey(on_delete=models.CASCADE, to="programme.Role"),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name="programmeedittoken",
            index_together={("person", "state")},
        ),
        migrations.AddField(
            model_name="programme",
            name="organizers",
            field=models.ManyToManyField(to="core.Person", through="programme.ProgrammeRole", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="programme",
            name="room",
            field=models.ForeignKey(
                on_delete=models.CASCADE, verbose_name="Tila", blank=True, to="programme.Room", null=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="programme",
            name="tags",
            field=models.ManyToManyField(to="programme.Tag", verbose_name="T\xe4git", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="category",
            name="event",
            field=models.ForeignKey(on_delete=models.CASCADE, to="core.Event"),
            preserve_default=True,
        ),
    ]
