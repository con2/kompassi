from django.db import models

from kompassi.core.utils import validate_slug
from kompassi.labour.models import SignupExtraBase
from kompassi.zombies.enrollment.models import SimpleChoice, SpecialDiet

SHIFT_TYPE_CHOICES = [
    ("yksipitka", "Yksi pitkä vuoro"),
    ("montalyhytta", "Monta lyhyempää vuoroa"),
    ("kaikkikay", "Kumpi tahansa käy"),
]

TOTAL_WORK_CHOICES = [
    ("8h", "8 tuntia - Täysvuoro"),
    ("yli10h", "Yli 10 tuntia - Supervuoro!"),
]


class Accommodation(SimpleChoice):
    pass


class WorkDay(SimpleChoice):
    pass


class KnownLanguage(SimpleChoice):
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
            "Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Huomaathan, ettei 4 tunnin työpanos oikeuta täysiin työvoimaetuihin. Tarkasta työvoimaedut Kotaen verkkosivuilta."
        ),
        choices=TOTAL_WORK_CHOICES,
    )

    night_shift = models.BooleanField(
        default=False,
        verbose_name="Olen valmis tekemään yötöitä klo 23-07",
    )

    overseer = models.BooleanField(
        default=False,
        verbose_name="Olen kiinnostunut vuorovastaavan tehtävistä",
        help_text=(
            "Vuorovastaavat ovat kokeneempia conityöläisiä, jotka toimivat oman tehtäväalueensa tiiminvetäjänä."
        ),
    )

    work_days = models.ManyToManyField(
        WorkDay,
        blank=True,
        verbose_name="Työskentelypäivät",
        help_text=("Merkitse ne päivät, jolloin olet käytettävissä vapaaehtoisena."),
        related_name="kotaeexpo2026_signup_extras",
    )

    want_certificate = models.BooleanField(
        default=False,
        verbose_name="Haluan todistuksen työskentelystäni",
    )

    known_language = models.ManyToManyField(
        KnownLanguage,
        blank=True,
        verbose_name="Osaamasi kielet",
        related_name="kotaeexpo2026_signup_extras",
    )

    known_language_other = models.TextField(
        blank=True,
        verbose_name="Muu kieli",
    )

    special_diet = models.ManyToManyField(
        SpecialDiet,
        blank=True,
        verbose_name="Erikoisruokavalio",
        related_name="kotaeexpo2026_signup_extras",
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

    accommodation = models.ManyToManyField(
        Accommodation,
        blank=True,
        verbose_name="Tarvitsen lattiamajoitusta",
        related_name="kotaeexpo2026_signup_extras",
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
            "Coniitit saavat käyttöönsä nick@kotae.fi-tyyppisen sähköpostialiaksen, joka "
            "ohjataan coniitin omaan sähköpostilaatikkoon. Tässä voit toivoa haluamaasi "
            "sähköpostialiaksen alkuosaa eli sitä, joka tulee ennen @kotae.fi:tä. "
            "Sallittuja merkkejä ovat pienet kirjaimet a-z, numerot 0-9 sekä väliviiva."
        ),
        validators=[validate_slug],
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm

    @classmethod
    def get_programme_form_class(cls):
        from .forms import ProgrammeSignupExtraForm

        return ProgrammeSignupExtraForm


class TimeSlot(SimpleChoice):
    pass


class AccessibilityWarning(SimpleChoice):
    pass
