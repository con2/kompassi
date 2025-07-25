# Generated by Django 1.10.8 on 2018-02-12 19:56
import django.db.models.deletion
from django.db import migrations, models

import kompassi.labour.models.signup_extras


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("labour", "0033_auto_20170802_1500"),
    ]

    operations = [
        migrations.CreateModel(
            name="SignupExtra",
            fields=[
                (
                    "signup",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="ropecon2018_signup_extra",
                        serialize=False,
                        to="labour.Signup",
                    ),
                ),
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
                    "extra_work",
                    models.CharField(
                        choices=[("miel", "Otan mielelläni varatyövoimavuoron"), ("ei", "En halua varatyövuoroa")],
                        help_text="Varatyövoiman päivystysvuoro on 4h, jonka aikana sinun tulee olla tavoitettavissa puhelimella Messukeskuksessa. Voit joutua mihin tahansa työpisteeseen paikkaamaan",
                        max_length=5,
                        verbose_name="Haluatko päivystää varatyövoimana?",
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
                        help_text="Jos haluat työtodistuksen, täytä tähän kenttään postiosoite (katuosoite, postinumero ja postitoimipaikka) johon haluat todistuksen toimitettavan.",
                        verbose_name="Työtodistuksen toimitusosoite",
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
                ("is_active", models.BooleanField(default=True)),
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
        migrations.AddField(
            model_name="signupextra",
            name="special_diet",
            field=models.ManyToManyField(blank=True, to="ropecon2018.SpecialDiet", verbose_name="Erikoisruokavalio"),
        ),
    ]
