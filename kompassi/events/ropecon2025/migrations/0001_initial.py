# Generated by Django 5.0.8 on 2024-08-18 17:24

import django.db.models.deletion
from django.db import migrations, models

import kompassi.labour.models.signup_extras


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0040_rename_emailverificationtoken_person_state_core_emailv_person__722147_idx_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Language",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=63)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SpecialDiet",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=63)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TimeSlot",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=63)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SignupExtra",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "shift_type",
                    models.CharField(
                        choices=[
                            ("yksipitka", "Yksi pitkä vuoro"),
                            ("montalyhytta", "Monta lyhyempää vuoroa"),
                            ("kaikkikay", "Kumpi tahansa käy"),
                        ],
                        help_text="Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?",
                        max_length=15,
                        verbose_name="Toivottu työvuoron pituus",
                    ),
                ),
                (
                    "total_work",
                    models.CharField(
                        choices=[
                            ("8h", "Minimi - 8 tuntia"),
                            ("12h", "10–12 tuntia"),
                            ("yli12h", "Työn Sankari! Yli 12 tuntia!"),
                        ],
                        help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Useimmissa tehtävistä minimi on kahdeksan tuntia, mutta joissain tehtävissä se voi olla myös vähemmän (esim. majoitusvalvonta 6 h).",
                        max_length=15,
                        verbose_name="Toivottu kokonaistyömäärä",
                    ),
                ),
                (
                    "want_certificate",
                    models.BooleanField(default=False, verbose_name="Haluan todistuksen työskentelystäni Ropeconissa"),
                ),
                (
                    "certificate_delivery_address",
                    models.TextField(
                        blank=True,
                        help_text="Todistukset toimitetaan ensisijaisesti sähköpostitse, mutta jos haluat todistuksesi paperilla kirjaa tähän postiosoite(katuosoite, postinumero ja toimipaikka), johon haluat todistuksen toimitettavan.",
                        verbose_name="Työtodistuksen toimitusosoite",
                    ),
                ),
                (
                    "other_languages",
                    models.TextField(
                        blank=True,
                        help_text="Please select those languages with which you feel comfortable doing customer service work and list those not listed in the free text field. You can also describe how proficient you are with those languages in the text field.",
                        verbose_name="Other languages",
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
                    "shift_wishes",
                    models.TextField(
                        blank=True,
                        help_text="Jos tiedät nyt jo, ettet pääse paikalle johonkin tiettyyn aikaan tai haluat osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siitä tässä.",
                        verbose_name="Alustavat työvuorotoiveet",
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
                    "roster_publish_consent",
                    models.BooleanField(
                        default=False,
                        verbose_name="I give my consent for Ropecon to publish my name to my co-workers in the volunteer roster of my assigned station.",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_signup_extras",
                        to="core.event",
                    ),
                ),
                ("languages", models.ManyToManyField(blank=True, to="ropecon2025.language", verbose_name="Kielet")),
                (
                    "person",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_signup_extra",
                        to="core.person",
                    ),
                ),
                (
                    "special_diet",
                    models.ManyToManyField(blank=True, to="ropecon2025.specialdiet", verbose_name="Erikoisruokavalio"),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(kompassi.labour.models.signup_extras.SignupExtraMixin, models.Model),
        ),
    ]
