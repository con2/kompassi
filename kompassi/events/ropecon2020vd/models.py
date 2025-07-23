from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.labour.models import SignupExtraBase
from kompassi.zombies.enrollment.models import SimpleChoice

TOTAL_WORK_CHOICES = [
    ("8h", "Minimi - 8 tuntia"),
    ("12h", "10–12 tuntia"),
    ("yli12h", "Työn Sankari! Yli 12 tuntia!"),
]

SHIFT_TYPE_CHOICES = [
    ("yksipitka", "Yksi pitkä vuoro"),
    ("montalyhytta", "Monta lyhyempää vuoroa"),
    ("kaikkikay", "Kumpi tahansa käy"),
]


class TimeSlot(SimpleChoice):
    pass


# class SpecialDiet(SimpleChoice):
#     pass


class SignupExtra(SignupExtraBase):
    # shift_type = models.CharField(max_length=15,
    #     verbose_name='Toivottu työvuoron pituus',
    #     help_text='Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?',
    #     choices=SHIFT_TYPE_CHOICES,
    # )

    total_work = models.CharField(
        max_length=15,
        verbose_name="Toivottu kokonaistyömäärä",
        help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Useimmissa tehtävistä minimi on kahdeksan tuntia, mutta joissain tehtävissä se voi olla myös vähemmän (esim. majoitusvalvonta 6 h).",
        choices=TOTAL_WORK_CHOICES,
    )

    want_certificate = models.BooleanField(
        default=False,
        verbose_name="Haluan todistuksen työskentelystäni Ropeconissa",
    )

    certificate_delivery_address = models.TextField(
        blank=True,
        verbose_name="Työtodistuksen toimitusosoite",
        help_text="Todistukset toimitetaan ensisijaisesti sähköpostitse, mutta jos haluat todistuksesi paperilla kirjaa tähän postiosoite(katuosoite, postinumero ja toimipaikka), johon haluat todistuksen toimitettavan.",
    )

    can_finnish = models.BooleanField(default=False, verbose_name=_("Finnish"))
    can_english = models.BooleanField(default=False, verbose_name=_("English"))
    other_languages = models.TextField(
        blank=True,
        verbose_name=_("Other languages"),
        help_text=_(
            "Please select those languages with which you feel comfortable doing customer service work and list those not listed in the free text field. You can also describe how proficient you are with those languages in the text field."
        ),
    )

    # special_diet = models.ManyToManyField(
    #     SpecialDiet,
    #     blank=True,
    #     verbose_name='Erikoisruokavalio'
    # )

    # special_diet_other = models.TextField(
    #     blank=True,
    #     verbose_name='Muu erikoisruokavalio',
    #     help_text='Jos noudatat erikoisruokavaliota, jota ei ole yllä olevassa listassa, '
    #     'ilmoita se tässä. Tapahtuman järjestäjä pyrkii ottamaan erikoisruokavaliot '
    #     'huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään.'
    # )

    prior_experience = models.TextField(
        blank=True,
        verbose_name="Työkokemus",
        help_text="Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista "
        "tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä "
        "hakemassasi tehtävässä.",
    )

    shift_wishes = models.TextField(
        blank=True,
        verbose_name="Alustavat työvuorotoiveet",
        help_text="Jos tiedät nyt jo, ettet pääse paikalle johonkin tiettyyn aikaan tai haluat "
        "osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siitä tässä.",
    )

    free_text = models.TextField(
        blank=True,
        verbose_name="Vapaa alue",
        help_text="Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole "
        "omaa kenttää yllä, käytä tätä kenttää.",
    )

    roster_publish_consent = models.BooleanField(
        default=False,
        verbose_name=_(
            "I give my consent for Ropecon to publish my name to my co-workers in the volunteer roster of my assigned station."
        ),
    )

    is_active = models.BooleanField(default=True)

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm

    @classmethod
    def get_programme_form_class(cls):
        from .forms import ProgrammeSignupExtraForm

        return ProgrammeSignupExtraForm
