from django.db import models

from enrollment.models import SimpleChoice, SpecialDiet
from labour.models import SignupExtraBase

from core.utils import validate_slug


SHIFT_TYPE_CHOICES = [
    ("yksipitka", "Yksi pitkä vuoro"),
    ("montalyhytta", "Monta lyhyempää vuoroa"),
    ("kaikkikay", "Kumpi tahansa käy"),
]

# TODO
TOTAL_WORK_CHOICES = [
    ("10h", "Minimi - 10 tuntia"),
    ("yli10h", "Työn Sankari! Yli 10 tuntia!"),
]

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
            "Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Minimi on pääsääntöisesti " "kymmenen tuntia."
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
        verbose_name="Haluan todistuksen työskentelystäni",
    )

    special_diet = models.ManyToManyField(
        SpecialDiet,
        blank=True,
        verbose_name="Erikoisruokavalio",
        related_name="kotaeexpo2024_signup_extras",
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

    # @classmethod
    # def get_programme_form_class(cls):
    #     from .forms import ProgrammeSignupExtraForm

    #     return ProgrammeSignupExtraForm
