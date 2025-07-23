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


class SpecialDiet(SimpleChoice):
    pass


class Language(SimpleChoice):
    pass


class SignupExtra(SignupExtraBase):
    shift_type = models.CharField(
        max_length=15,
        verbose_name="Toivottu työvuoron pituus",
        help_text=_("Would you like to work one long shift or multiple shorter shifts?"),
        choices=SHIFT_TYPE_CHOICES,
    )

    total_work = models.CharField(
        max_length=15,
        verbose_name="Toivottu kokonaistyömäärä",
        help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Useimmissa tehtävistä minimi on kahdeksan tuntia, mutta joissain tehtävissä se voi olla myös vähemmän (esim. majoitusvalvonta 6 h).",
        choices=TOTAL_WORK_CHOICES,
    )

    want_certificate = models.BooleanField(
        default=False,
        verbose_name="Haluan todistuksen työskentelystäni Ropeconissa",
        help_text=_("Work certificates will be sent to the email address provided after the event."),
    )

    languages = models.ManyToManyField(Language, blank=True, verbose_name="Kielet")
    other_languages = models.TextField(
        blank=True,
        verbose_name=_("Other languages"),
        help_text=_(
            "Please select those languages with which you feel comfortable doing customer service work and list those not listed in the free text field. You can also describe how proficient you are with those languages in the text field."
        ),
    )

    special_diet = models.ManyToManyField(SpecialDiet, blank=True, verbose_name="Erikoisruokavalio")

    special_diet_other = models.TextField(
        blank=True,
        verbose_name="Muu erikoisruokavalio",
        help_text=_(
            "If you are on a special diet that is not listed above, you can add it here. The event organizers will take special dietary needs into consideration, but it may not be possible to cater to all of them."
        ),
    )

    prior_experience = models.TextField(
        blank=True,
        verbose_name="Työkokemus",
        help_text=_(
            "If you have work, volunteer work or other experience you think might be useful in the work station you are applying for, you can provide the information here."
        ),
    )

    shift_wishes = models.TextField(
        blank=True,
        verbose_name="Alustavat työvuorotoiveet",
        help_text=_(
            "If you already know that you will not be able to attend a certain time or want to participate in a programme, you can provide the information here. Note that depending on the workstation, shifts may also take place before and after the event opening hours (on Thursday, Friday morning and Sunday evening) as well as during the nighttime (between 10:00 PM and 6:00 AM). Final shift preference surveys will be sent out in the summer after the programme for Ropecon 2025 is published."
        ),
    )

    free_text = models.TextField(
        blank=True,
        verbose_name="Vapaa alue",
        help_text="If you want to share something to the application reviewers that doesn't have a dedicated field above, please use this field.",
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
        raise NotImplementedError("Ropecon 2025 does not support Programme V1")
