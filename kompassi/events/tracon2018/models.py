from django.db import models

from kompassi.core.utils import validate_slug
from kompassi.labour.models import SignupExtraBase
from kompassi.zombies.enrollment.models import SimpleChoice, SpecialDiet

SHIRT_SIZES = [
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
]

SHIFT_TYPE_CHOICES = [
    ("yksipitka", "Yksi pitkä vuoro"),
    ("montalyhytta", "Monta lyhyempää vuoroa"),
    ("kaikkikay", "Kumpi tahansa käy"),
]

TOTAL_WORK_CHOICES = [
    ("10h", "Minimi - 10 tuntia"),
    ("yli10h", "Työn Sankari! Yli 10 tuntia!"),
]


class Night(SimpleChoice):
    pass


class Poison(SimpleChoice):
    pass


class SignupExtra(SignupExtraBase):
    shift_type = models.CharField(
        max_length=15,
        verbose_name="Toivottu työvuoron pituus",
        help_text="Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?",
        choices=SHIFT_TYPE_CHOICES,
    )

    total_work = models.CharField(
        max_length=15,
        verbose_name="Toivottu kokonaistyömäärä",
        help_text=(
            "Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Minimi on pääsääntöisesti kymmenen tuntia."
        ),
        choices=TOTAL_WORK_CHOICES,
    )

    overseer = models.BooleanField(
        default=False,
        verbose_name="Olen kiinnostunut vuorovastaavan tehtävistä",
        help_text=(
            "Vuorovastaavat ovat kokeneempia conityöläisiä, jotka toimivat oman tehtäväalueensa tiiminvetäjänä."
        ),
    )

    want_certificate = models.BooleanField(
        default=False,
        verbose_name="Haluan todistuksen työskentelystäni Traconissa",
    )

    certificate_delivery_address = models.TextField(
        blank=True,
        verbose_name="Työtodistuksen toimitusosoite",
        help_text=(
            "Jos haluat työtodistuksen, täytä tähän kenttään postiosoite (katuosoite, "
            "postinumero ja postitoimipaikka) johon haluat todistuksen toimitettavan."
        ),
    )

    shirt_size = models.CharField(
        max_length=8,
        choices=SHIRT_SIZES,
        default="NO_SHIRT",
        verbose_name="Paidan koko",
        help_text=(
            "Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan. "
            'Kokotaulukot: <a href="http://www.bc-collection.eu/uploads/sizes/TU004.jpg" '
            'target="_blank">unisex-paita</a>, <a href="http://www.bc-collection.eu/uploads/sizes/TW040.jpg" '
            'target="_blank">ladyfit-paita</a>'
        ),
    )

    special_diet = models.ManyToManyField(SpecialDiet, blank=True, verbose_name="Erikoisruokavalio", related_name="+")

    special_diet_other = models.TextField(
        blank=True,
        verbose_name="Muu erikoisruokavalio",
        help_text=(
            "Jos noudatat erikoisruokavaliota, jota ei ole yllä olevassa listassa, "
            "ilmoita se tässä. Tapahtuman järjestäjä pyrkii ottamaan erikoisruokavaliot "
            "huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään."
        ),
    )

    lodging_needs = models.ManyToManyField(
        Night,
        blank=True,
        verbose_name="Tarvitsen lattiamajoitusta",
        help_text=(
            "Ruksaa ne yöt, joille tarvitset lattiamajoitusta. Lattiamajoitus sijaitsee "
            "kävelymatkan päässä tapahtumapaikalta."
        ),
    )

    prior_experience = models.TextField(
        blank=True,
        verbose_name="Työkokemus",
        help_text=(
            "Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista "
            "tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä "
            "hakemassasi tehtävässä."
        ),
    )

    free_text = models.TextField(
        blank=True,
        verbose_name="Vapaa alue",
        help_text=(
            "Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole "
            "omaa kenttää yllä, käytä tätä kenttää."
        ),
    )

    shift_wishes = models.TextField(
        blank=True,
        verbose_name="Työvuorotoiveet",
        help_text=(
            "Jos tiedät, ettet pääse paikalle johonkin tiettyyn aikaan tai haluat esimerkiksi "
            "osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siitä tässä."
        ),
    )

    email_alias = models.CharField(
        blank=True,
        default="",
        max_length=32,
        verbose_name="Sähköpostialias",
        help_text=(
            "Coniitit saavat käyttöönsä nick@tracon.fi-tyyppisen sähköpostialiaksen, joka "
            "ohjataan coniitin omaan sähköpostilaatikkoon. Tässä voit toivoa haluamaasi "
            "sähköpostialiaksen alkuosaa eli sitä, joka tulee ennen @tracon.fi:tä. "
            "Sallittuja merkkejä ovat pienet kirjaimet a-z, numerot 0-9 sekä väliviiva."
        ),
        validators=[validate_slug],
    )

    afterparty_participation = models.BooleanField(
        default=False,
        verbose_name="Osallistun kaatajaisiin",
        help_text=(
            "Ruksaa tämä ruutu, mikäli haluat osallistua kaatajaisiin. Mikäli mielesi muuttuu "
            "tai sinulle tulee este, peru ilmoittautumisesi poistamalla rasti tästä ruudusta."
        ),
    )

    outward_coach_departure_time = models.CharField(
        blank=True,
        default="",
        max_length=5,
        choices=[
            ("16:00", "16:00"),
            ("17:00", "17:00"),
            ("18:00", "18:00"),
            ("nobus", "En tarvitse menokyytiä (tulen omalla kyydillä)"),
        ],
        verbose_name="Menobussin lähtöaika",
    )

    return_coach_departure_time = models.CharField(
        blank=True,
        default="",
        max_length=5,
        choices=[
            ("23:00", "23:00"),
            ("00:00", "00:00"),
            ("01:00", "01:00"),
            ("nobus", "En tarvitse paluukyytiä (poistun omalla kyydillä)"),
        ],
        verbose_name="Paluubussin lähtöaika",
        help_text=(
            "Tracon tarjoaa maksuttoman bussikyydin kaatajaisiin ja takaisin Tampereen keskustorilta. "
            "Saavuthan hyvissä ajoin ennen valitsemaasi lähtöaikaa lähtöpysäkille (Vanha kirkko), ja "
            "huolehdithan itse siitä, että nouset oikeaan aikaan paluubussiin kaatajaispaikalla. Mikäli myöhästyt "
            "valitsemastasi bussista, Tracon ei välttämättä pysty tarjoamaan sinulle kyytiä kaatajaisiin "
            "tai sieltä pois. Bussit täytetään ilmoittautumisjärjestyksessä, ja mikäli jokin busseista "
            "osoittautuu erityisen suosituksi, saatamme joutua siirtämään osallistujia bussista toiseen, "
            "mistä ilmoitamme sähköpostitse. Meno- tai paluubussin vaihto kaatajaisilmoittautumisen sulkeuduttua "
            "ainoastaan kaatajaisvastaavan myötävaikutuksella os. kaatajaiset@tracon.fi, ei omin päin."
        ),
    )

    afterparty_coaches_changed = models.BooleanField(
        default=False,
    )

    pick_your_poison = models.ManyToManyField(
        Poison,
        blank=True,
        verbose_name="Mitä tykkäät juoda?",
        help_text=(
            "Pyrimme siihen, että kaikki löytäisivät kaadon tarjoiluista jotain itselleen sopivaa. Ruksaa "
            "kaikki ne juomat, mitä saattaisit kuvitella nauttivasi kaadon aikana, niin yritämme arvioida "
            "määriä jotenkin sinne päin. Huomaathan kuitenkin, että haluamme pitää kaadon kaikille mukavana "
            "ja turvallisena, eikä kaadossa ole tarkoitus juoda itseään örveltäväksi idiootiksi."
        ),
    )

    willing_to_bartend = models.BooleanField(
        default=False,
        verbose_name="Olen halukas tekemään 1h juomienkaatonakin kaatajaisissa",
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm

    @classmethod
    def get_programme_form_class(cls):
        from .forms import ProgrammeSignupExtraForm

        return ProgrammeSignupExtraForm

    @property
    def formatted_lodging_needs(self):
        return "\n".join(
            "{night}: {need}".format(
                night=night.name,
                need=(
                    "Tarvitsee lattiamajoitusta"
                    if self.lodging_needs.filter(pk=night.pk).exists()
                    else "Ei tarvetta lattiamajoitukselle"
                ),
            )
            for night in Night.objects.all()
        )
