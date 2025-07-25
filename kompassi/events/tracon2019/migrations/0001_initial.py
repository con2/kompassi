# Generated by Django 1.10.8 on 2018-09-26 09:52
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import kompassi.labour.models.signup_extras


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0030_auto_20180926_1252"),
        ("enrollment", "0005_auto_20170928_1334"),
    ]

    operations = [
        migrations.CreateModel(
            name="Night",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=63)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Poison",
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
                ("is_active", models.BooleanField(default=True)),
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
                        choices=[("10h", "Minimi - 10 tuntia"), ("yli10h", "Työn Sankari! Yli 10 tuntia!")],
                        help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Minimi on pääsääntöisesti kymmenen tuntia.",
                        max_length=15,
                        verbose_name="Toivottu kokonaistyömäärä",
                    ),
                ),
                (
                    "overseer",
                    models.BooleanField(
                        default=False,
                        help_text="Vuorovastaavat ovat kokeneempia conityöläisiä, jotka toimivat oman tehtäväalueensa tiiminvetäjänä.",
                        verbose_name="Olen kiinnostunut vuorovastaavan tehtävistä",
                    ),
                ),
                (
                    "want_certificate",
                    models.BooleanField(default=False, verbose_name="Haluan todistuksen työskentelystäni Traconissa"),
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
                    "shirt_size",
                    models.CharField(
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
                        ],
                        default="NO_SHIRT",
                        help_text='Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan. Kokotaulukot: <a href="http://www.bc-collection.eu/uploads/sizes/TU004.jpg" target="_blank">unisex-paita</a>, <a href="http://www.bc-collection.eu/uploads/sizes/TW040.jpg" target="_blank">ladyfit-paita</a>',
                        max_length=8,
                        verbose_name="Paidan koko",
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
                    "free_text",
                    models.TextField(
                        blank=True,
                        help_text="Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole omaa kenttää yllä, käytä tätä kenttää.",
                        verbose_name="Vapaa alue",
                    ),
                ),
                (
                    "shift_wishes",
                    models.TextField(
                        blank=True,
                        help_text="Jos tiedät, ettet pääse paikalle johonkin tiettyyn aikaan tai haluat esimerkiksi osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siitä tässä.",
                        verbose_name="Työvuorotoiveet",
                    ),
                ),
                (
                    "email_alias",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Coniitit saavat käyttöönsä nick@tracon.fi-tyyppisen sähköpostialiaksen, joka ohjataan coniitin omaan sähköpostilaatikkoon. Tässä voit toivoa haluamaasi sähköpostialiaksen alkuosaa eli sitä, joka tulee ennen @tracon.fi:tä. Sallittuja merkkejä ovat pienet kirjaimet a-z, numerot 0-9 sekä väliviiva.",
                        max_length=32,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Tekninen nimi saa sisältää vain pieniä kirjaimia, numeroita sekä väliviivoja.",
                                regex="[a-z0-9-]+",
                            )
                        ],
                        verbose_name="Sähköpostialias",
                    ),
                ),
                (
                    "afterparty_participation",
                    models.BooleanField(
                        default=False,
                        help_text="Ruksaa tämä ruutu, mikäli haluat osallistua kaatajaisiin. Mikäli mielesi muuttuu tai sinulle tulee este, peru ilmoittautumisesi poistamalla rasti tästä ruudusta.",
                        verbose_name="Osallistun kaatajaisiin",
                    ),
                ),
                (
                    "outward_coach_departure_time",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("16:00", "16:00"),
                            ("17:00", "17:00"),
                            ("18:00", "18:00"),
                            ("nobus", "En tarvitse menokyytiä (tulen omalla kyydillä)"),
                        ],
                        default="",
                        max_length=5,
                        verbose_name="Menobussin lähtöaika",
                    ),
                ),
                (
                    "return_coach_departure_time",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("23:00", "23:00"),
                            ("00:00", "00:00"),
                            ("01:00", "01:00"),
                            ("nobus", "En tarvitse paluukyytiä (poistun omalla kyydillä)"),
                        ],
                        default="",
                        help_text="Tracon tarjoaa maksuttoman bussikyydin kaatajaisiin ja takaisin Tampereen keskustorilta. Saavuthan hyvissä ajoin ennen valitsemaasi lähtöaikaa lähtöpysäkille (Vanha kirkko), ja huolehdithan itse siitä, että nouset oikeaan aikaan paluubussiin kaatajaispaikalla. Mikäli myöhästyt valitsemastasi bussista, Tracon ei välttämättä pysty tarjoamaan sinulle kyytiä kaatajaisiin tai sieltä pois. Bussit täytetään ilmoittautumisjärjestyksessä, ja mikäli jokin busseista osoittautuu erityisen suosituksi, saatamme joutua siirtämään osallistujia bussista toiseen, mistä ilmoitamme sähköpostitse. Meno- tai paluubussin vaihto kaatajaisilmoittautumisen sulkeuduttua ainoastaan kaatajaisvastaavan myötävaikutuksella os. kaatajaiset@tracon.fi, ei omin päin.",
                        max_length=5,
                        verbose_name="Paluubussin lähtöaika",
                    ),
                ),
                ("afterparty_coaches_changed", models.BooleanField(default=False)),
                (
                    "willing_to_bartend",
                    models.BooleanField(
                        default=False, verbose_name="Olen halukas tekemään 1h juomienkaatonakin kaatajaisissa"
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tracon2019_signup_extras",
                        to="core.Event",
                    ),
                ),
                (
                    "lodging_needs",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Ruksaa ne yöt, joille tarvitset lattiamajoitusta. Lattiamajoitus sijaitsee kävelymatkan päässä tapahtumapaikalta.",
                        to="tracon2019.Night",
                        verbose_name="Tarvitsen lattiamajoitusta",
                    ),
                ),
                (
                    "person",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tracon2019_signup_extra",
                        to="core.Person",
                    ),
                ),
                (
                    "pick_your_poison",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Pyrimme siihen, että kaikki löytäisivät kaadon tarjoiluista jotain itselleen sopivaa. Ruksaa kaikki ne juomat, mitä saattaisit kuvitella nauttivasi kaadon aikana, niin yritämme arvioida määriä jotenkin sinne päin. Huomaathan kuitenkin, että haluamme pitää kaadon kaikille mukavana ja turvallisena, eikä kaadossa ole tarkoitus juoda itseään örveltäväksi idiootiksi.",
                        to="tracon2019.Poison",
                        verbose_name="Mitä tykkäät juoda?",
                    ),
                ),
                (
                    "special_diet",
                    models.ManyToManyField(
                        blank=True,
                        related_name="tracon2019_signup_extras",
                        to="enrollment.SpecialDiet",
                        verbose_name="Erikoisruokavalio",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(kompassi.labour.models.signup_extras.SignupExtraMixin, models.Model),
        ),
    ]
