from django.db import models

from kompassi.labour.models import SignupExtraBase


class SignupExtra(SignupExtraBase):
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

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm
