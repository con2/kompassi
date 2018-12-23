from django.db import models

from labour.models import SignupExtraBase


class SignupExtra(SignupExtraBase):
    prior_experience = models.TextField(
        blank=True,
        verbose_name='Työkokemus',
        help_text=(
            'Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista '
            'tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä '
            'hakemassasi tehtävässä.'
        ),
    )

    shift_wishes = models.TextField(
        blank=True,
        verbose_name='Työvuorotoiveet',
        help_text=(
            'Jos tiedät nyt jo, ettet pääse paikalle johonkin tiettyyn aikaan tai haluat '
            'osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siitä tässä.'
        ),
    )

    free_text = models.TextField(
        blank=True,
        verbose_name='Vapaa alue',
        help_text=(
            'Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole '
            'omaa kenttää yllä, käytä tätä kenttää.'
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
