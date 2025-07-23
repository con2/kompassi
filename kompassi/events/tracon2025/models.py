from django.db import models

from kompassi.core.utils import validate_slug
from kompassi.labour.models import SignupExtraBase
from kompassi.zombies.enrollment.models import SimpleChoice, SpecialDiet

SHIRT_SIZES = [
    ("NO_SHIRT", "Ei paitaa"),
    # ("BOTTLE", "Juomapullo"),
    ("XS", "XS Unisex"),
    ("S", "S Unisex"),
    ("M", "M Unisex"),
    ("L", "L Unisex"),
    ("XL", "XL Unisex"),
    ("XXL", "2XL Unisex"),
    ("3XL", "3XL Unisex"),
    ("4XL", "4XL Unisex"),
    ("5XL", "5XL Unisex"),
    ("LF_XS", "XS Ladyfit"),
    ("LF_S", "S Ladyfit"),
    ("LF_M", "M Ladyfit"),
    ("LF_L", "L Ladyfit"),
    ("LF_XL", "XL Ladyfit"),
    ("LF_XXL", "2XL Ladyfit"),
    ("LF_3XL", "3XL Ladyfit"),
    ("BAG", "Kangaskassi"),
]

SHIFT_TYPE_CHOICES = [
    ("yksipitka", "Yksi pitkä vuoro"),
    ("montalyhytta", "Monta lyhyempää vuoroa"),
    ("kaikkikay", "Kumpi tahansa käy"),
]

TOTAL_WORK_CHOICES = [
    ("10h", "10h minimi - 2 ruokalippua, 1 työvoimatuote"),
    ("12h", "12h - 3 ruokalippua, 1 työvoimatuote"),
    ("14h", "14h - 3 ruokalippua, 2 työvoimatuotetta"),
    ("16h", "16h - 4 ruokalippua, 2 työvoimatuotetta"),
]


class Night(SimpleChoice):
    pass


class Poison(SimpleChoice):
    pass


class TimeSlot(SimpleChoice):
    pass


class AccessibilityWarning(SimpleChoice):
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

    shirt_size = models.CharField(
        max_length=8,
        choices=SHIRT_SIZES,
        default="NO_SHIRT",
        verbose_name="Swag-valinta",
        help_text=(
            "Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan tai kangaskassin. "
            "Valitse tässä haluatko paidan vai kangaskassin, sekä paidan koko. "
            '<a href="/static/tracon2022/tracon2022_shirt_sizes.png" target="_blank" rel="noopener noreferrer">Kokotaulukko</a>'
        ),
    )

    special_diet = models.ManyToManyField(
        SpecialDiet,
        blank=True,
        verbose_name="Erikoisruokavalio",
        related_name="tracon2025_signup_extras",
    )

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
            "osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siitä tässä. HUOM! Muistathan "
            "mainita kellonajat (myös ohjelmanumeroista)."
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
            "tai sinulle tulee este, peru ilmoittautumisesi poistamalla rasti tästä ruudusta. "
            'Muistathan tällöin vapauttaa myös mahdollisen <a href="/profile/reservations" target="_blank">paikkasi kaatobussissa</a>.'
        ),
    )

    afterparty_policy = models.BooleanField(
        default=False,
        verbose_name=(
            "Olen tutustunut Traconin häirinnän vastaiseen linjaukseen, "
            "ymmärrän sen olevan voimassa myös kaadossa ja sitoudun noudattamaan sitä."
        ),
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

    afterparty_help = models.TextField(
        default="",
        verbose_name="Työskentely kaatajaisissa",
        blank=True,
        help_text=(
            "Kaatajaiset järjestyvät oman työryhmän voimin, mutta joskus lisäkädet ovat tarpeen. "
            "Oletko valmis auttamaan kaadon järjestelyissä, esim. logistiikassa tai juomien kaatamisessa? "
            "Jos kyllä, kirjoita tähän. "
            "Erityisesti pulaa on usein paluukuskeista, niin omalla autolla kuin ilman omaa autoa raittiina liikkeellä olevista. "
            "Vastanneisiin otetaan yhteyttä Slackitse jos apuanne tarvitaan."
        ),
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
