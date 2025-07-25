# Generated by Django 1.10.8 on 2018-10-03 13:54
import django.db.models.deletion
from django.db import migrations, models

import kompassi.labour.models.signup_extras


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0030_auto_20180926_1252"),
    ]

    operations = [
        migrations.CreateModel(
            name="SignupExtra",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_active", models.BooleanField(default=True)),
                (
                    "shift_type",
                    models.CharField(
                        choices=[
                            ("2h", "2 tunnin vuoroja"),
                            ("4h", "4 tunnin vuoroja"),
                            ("yli4h", "Yli 4 tunnin vuoroja"),
                        ],
                        help_text="Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?",
                        max_length=15,
                        verbose_name="Toivottu työvuoron pituus",
                    ),
                ),
                (
                    "total_work",
                    models.CharField(
                        choices=[("4h", "4–8 tuntia"), ("8h", "8 tuntia"), ("yli8h", "Yli 8 tuntia")],
                        help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana?",
                        max_length=15,
                        verbose_name="Toivottu kokonaistyömäärä",
                    ),
                ),
                (
                    "shirt_size",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NO_SHIRT", "Ei paitaa"),
                            ("XS", "XS Unisex"),
                            ("S", "S Unisex"),
                            ("M", "M Unisex"),
                            ("L", "L Unisex"),
                            ("XL", "XL Unisex"),
                            ("XXL", "XXL Unisex"),
                            ("3XL", "3XL Unisex"),
                            ("4XL", "4XL Unisex"),
                            ("5XL", "5XL Unisex"),
                            ("LF_XS", "XS Ladyfit"),
                            ("LF_S", "S Ladyfit"),
                            ("LF_M", "M Ladyfit"),
                            ("LF_L", "L Ladyfit"),
                            ("LF_XL", "XL Ladyfit"),
                            ("LF_2XL", "2XL Ladyfit"),
                            ("LF_3XL", "3XL Ladyfit"),
                        ],
                        help_text="Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan, mikäli ilmoittavat työskentelevänsä vähintään 8 tuntia.",
                        max_length=8,
                        null=True,
                        verbose_name="Paidan koko",
                    ),
                ),
                (
                    "dead_dog",
                    models.BooleanField(
                        default=False,
                        help_text="Dead dogit ovat heti tapahtuman jälkeen järjestettävät kestit kaikille täysikäisille työvoimaan kuuluville. Ilmoittautuminen ei ole sitova.",
                        verbose_name="Osallistun dead dogeihin",
                    ),
                ),
                (
                    "special_diet_other",
                    models.TextField(
                        blank=True,
                        help_text="Jos noudatat erikoisruokavaliota, jota ei ole yllä olevassa listassa, ilmoita se tässä. Tapahtuman järjestäjä pyrkii ottamaan erikoisruokavaliot huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään.",
                        verbose_name="Muu erikoisruokavalio",
                    ),
                ),
                (
                    "prior_experience",
                    models.TextField(
                        blank=True,
                        help_text="Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä hakemassasi tehtävässä.",
                        verbose_name="Työkokemus",
                    ),
                ),
                (
                    "language_skills",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Kerro kielitaidostasi erityisesti suomen, ruotsin ja englannin kielissä.",
                        verbose_name="Kielitaito",
                    ),
                ),
                (
                    "free_text",
                    models.TextField(
                        blank=True,
                        help_text="Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole omaa kenttää yllä, käytä tätä kenttää.",
                        verbose_name="Vapaa alue",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="finncon2020_signup_extras",
                        to="core.Event",
                    ),
                ),
                (
                    "person",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="finncon2020_signup_extra",
                        to="core.Person",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(kompassi.labour.models.signup_extras.SignupExtraMixin, models.Model),
        ),
        migrations.CreateModel(
            name="SpecialDiet",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=63)),
            ],
        ),
        migrations.AddField(
            model_name="signupextra",
            name="special_diet",
            field=models.ManyToManyField(blank=True, to="finncon2020.SpecialDiet", verbose_name="Erikoisruokavalio"),
        ),
    ]
