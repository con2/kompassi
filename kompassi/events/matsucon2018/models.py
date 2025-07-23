from django.db import models

from kompassi.labour.models import SignupExtraBase

SHIRT_SIZES = [
    ("NO_SHIRT", "En halua paitaa"),
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("OTHER", "Muu koko (kerro Vapaa sana -kentässä)"),
]

SHIFT_TYPE_CHOICES = [
    ("lb", "Pitkät vuorot molempina päivinä (4h/vuoro/päivä)"),
    ("sb", "Lyhyitä vuoroja molempina päivinä (2h/vuoro, 4h/päivä)"),
    ("as", "Kaikki vuorot lauantaina"),
    ("au", "Kaikki vuorot sunnuntaina"),
]


class SignupExtra(SignupExtraBase):
    want_certificate = models.BooleanField(
        default=False,
        verbose_name="Haluan todistuksen työskentelystäni Matsuconissa",
    )

    shirt_size = models.CharField(
        max_length=8,
        choices=SHIRT_SIZES,
        default="NO_SHIRT",
        verbose_name="Työvoiman T-paidan koko",
    )

    special_diet = models.ManyToManyField(
        "enrollment.SpecialDiet",
        blank=True,
        verbose_name="Erikoisruokavalio",
        related_name="%(app_label)s_%(class)s",
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

    shift_type = models.CharField(
        max_length=2,
        choices=SHIFT_TYPE_CHOICES,
        verbose_name="Valitse toivomasi työvuoro",
        help_text=(
            "Jokaisen työvoimaan kuuluvan on tehtävä vähintään 8 tuntia töitä. Työvuorotoiveet "
            "yritetään huomioida vuoroja jaettaessa. Jos haluat kaikki vuorot samalle päivälle, vuorot "
            "jaetaan niin että pääset pitämään taukoa välissä."
        ),
    )

    night_work = models.BooleanField(
        verbose_name="Olen valmis tekemään yötyötä (jos valitsit työn, joka sellaista sisältää)",
        default=False,
    )

    need_lodging = models.BooleanField(
        verbose_name="Tarvitsen majoituksen (lattiamajoitus)",
        default=False,
    )

    more_info = models.TextField(
        blank=True,
        default="",
        verbose_name="Lisätietoja osaamisestasi",
        help_text=(
            "Jos valitsit työn, joka tarvitsee selvennystä osaamisestasi (ensiapukortti, linkki "
            "portfolioon jne.), kirjoita siitä tähän."
        ),
    )

    prior_experience = models.TextField(
        blank=True,
        verbose_name="Työkokemus",
        help_text=("Oletko tehnyt vastaavaa työtä aikaisemmin? Muuta hyödyllistä työkokemusta? Kerro itsestäsi!"),
    )

    free_text = models.TextField(
        blank=True,
        verbose_name="Vapaa sana",
        help_text="Muuta kerrottavaa? Kysyttävää? Kirjoita se tähän.",
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm

    @classmethod
    def get_programme_form_class(cls):
        from .forms import ProgrammeSignupExtraForm

        return ProgrammeSignupExtraForm
