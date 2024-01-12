# Generated by Django 2.2.9 on 2020-03-05 19:47

from django.db import migrations, models
import django.db.models.deletion
import labour.models.signup_extras


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("enrollment", "0008_auto_20190409_2051"),
        ("core", "0033_auto_20191111_1851"),
    ]

    operations = [
        migrations.CreateModel(
            name="SignupExtra",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_active", models.BooleanField(default=True)),
                (
                    "want_certificate",
                    models.BooleanField(default=False, verbose_name="Haluan todistuksen työskentelystäni Matsuconissa"),
                ),
                (
                    "shirt_size",
                    models.CharField(
                        choices=[
                            ("NO_SHIRT", "En halua paitaa"),
                            ("S", "S"),
                            ("M", "M"),
                            ("L", "L"),
                            ("XL", "XL"),
                            ("OTHER", "Muu koko (kerro Vapaa sana -kentässä)"),
                        ],
                        default="NO_SHIRT",
                        max_length=8,
                        verbose_name="Työvoiman T-paidan koko",
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
                    "shift_type",
                    models.CharField(
                        choices=[
                            ("lb", "Pitkät vuorot molempina päivinä (4h/vuoro/päivä)"),
                            ("sb", "Lyhyitä vuoroja molempina päivinä (2h/vuoro, 4h/päivä)"),
                            ("as", "Kaikki vuorot lauantaina"),
                            ("au", "Kaikki vuorot sunnuntaina"),
                        ],
                        help_text="Jokaisen työvoimaan kuuluvan on tehtävä vähintään 8 tuntia töitä. Työvuorotoiveet yritetään huomioida vuoroja jaettaessa. Jos haluat kaikki vuorot samalle päivälle, vuorot jaetaan niin että pääset pitämään taukoa välissä.",
                        max_length=2,
                        verbose_name="Valitse toivomasi työvuoro",
                    ),
                ),
                (
                    "night_work",
                    models.BooleanField(
                        default=False,
                        verbose_name="Olen valmis tekemään yötyötä (jos valitsit työn, joka sellaista sisältää)",
                    ),
                ),
                (
                    "need_lodging",
                    models.BooleanField(default=False, verbose_name="Tarvitsen majoituksen (lattiamajoitus)"),
                ),
                (
                    "more_info",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Jos valitsit työn, joka tarvitsee selvennystä osaamisestasi (ensiapukortti, linkki portfolioon jne.), kirjoita siitä tähän.",
                        verbose_name="Lisätietoja osaamisestasi",
                    ),
                ),
                (
                    "prior_experience",
                    models.TextField(
                        blank=True,
                        help_text="Oletko tehnyt vastaavaa työtä aikaisemmin? Muuta hyödyllistä työkokemusta? Kerro itsestäsi!",
                        verbose_name="Työkokemus",
                    ),
                ),
                (
                    "free_text",
                    models.TextField(
                        blank=True,
                        help_text="Muuta kerrottavaa? Kysyttävää? Kirjoita se tähän.",
                        verbose_name="Vapaa sana",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="matsucon2020_signup_extras",
                        to="core.Event",
                    ),
                ),
                (
                    "person",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="matsucon2020_signup_extra",
                        to="core.Person",
                    ),
                ),
                (
                    "special_diet",
                    models.ManyToManyField(
                        blank=True,
                        related_name="matsucon2020_signupextra",
                        to="enrollment.SpecialDiet",
                        verbose_name="Erikoisruokavalio",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(labour.models.signup_extras.SignupExtraMixin, models.Model),
        ),
    ]
