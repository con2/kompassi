from django.db import models
from kompassi.labour.models import SignupExtraBase


class SignupExtra(SignupExtraBase):
    special_diet = models.TextField(
        blank=True,
        verbose_name="Erikoisruokavalio",
    )

    prior_experience = models.TextField(
        blank=True,
        verbose_name="Aikaisempi kokemus",
    )

    free_text = models.TextField(
        blank=True,
        verbose_name="Vapaa sana",
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm
        return SignupExtraForm
