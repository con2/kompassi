from django.db import models

from kompassi.labour.models import SignupExtraBase
from kompassi.zombies.enrollment.models import SimpleChoice, SpecialDiet


class WorkDay(SimpleChoice):
    pass


class SignupExtra(SignupExtraBase):
    work_days = models.ManyToManyField(
        WorkDay,
        blank=True,
        verbose_name="Toivotut vapaaehtoistyöpäivät",
        help_text=(
            "Merkitse ne päivät, joina olet käytettävissä vapaaehtoisena. Jos sinulle käy mikä "
            "tahansa päivä, merkitse ne kaikki. Toiveita pyritään toteuttamaan mahdollisuuksien "
            "puitteissa."
        ),
        related_name="cosmocon2027_signup_extras",
    )

    special_diet = models.ManyToManyField(
        SpecialDiet,
        blank=True,
        verbose_name="Erikoisruokavalio",
        related_name="cosmocon2027_signup_extras",
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

    friend_wish = models.TextField(
        blank=True,
        verbose_name="Kaveritoive",
        help_text=(
            "Jos haluaisit työskennellä samassa vuorossa jonkun tietyn henkilön kanssa, kerro se "
            "tässä. Toiveita pyritään toteuttamaan mahdollisuuksien puitteissa."
        ),
    )

    free_text = models.TextField(
        blank=True,
        verbose_name="Vapaa sana",
        help_text=(
            "Onko jotain muuta, jota conitean tai vapaaehtoisvuorosi vastaavan olisi hyvä tietää "
            "ja joka etenkin vaikuttaa vapaaehtoistyöskentelyysi? Kirjoita se tähän."
        ),
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm
