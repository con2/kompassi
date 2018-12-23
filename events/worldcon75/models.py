# encoding: utf-8

from django.db import models

from labour.models import SignupExtraBase


class SignupExtra(SignupExtraBase):
    special_diet = models.ManyToManyField(
        'enrollment.SpecialDiet',
        blank=True,
        verbose_name='Erikoisruokavalio',
        related_name='%(app_label)s_%(class)s',
    )

    special_diet_other = models.TextField(
        blank=True,
        verbose_name='Muu erikoisruokavalio',
        help_text=(
            'Jos noudatat erikoisruokavaliota, jota ei ole yllä olevassa listassa, '
            'ilmoita se tässä. Tapahtuman järjestäjä pyrkii ottamaan erikoisruokavaliot '
            'huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään.'
        )
    )

    shift_wishes = models.TextField(
        blank=True,
        verbose_name='Työvuorotoiveet',
        help_text=(
            'Miten olet käytettävissä työvuoroihin tapahtuman aikana? '
            'Jos tiedät, ettet pääse paikalle johonkin tiettyyn aikaan tai haluat esimerkiksi '
            'osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siitä tässä.'
        ),
    )

    prior_experience = models.TextField(
        blank=True,
        verbose_name='Työkokemus',
        help_text=(
            'Kerro aikaisemmasta työkokemuksestasi tapahtuman työvoimana tai muusta kokemuksesta, '
            'josta koet olevan hyötyä haetussa/haetuissa työtehtävissä.'
        ),
    )

    free_text = models.TextField(
        blank=True,
        verbose_name='Lisätietoja',
        help_text='Tässä kentässä voit kertoa jotain minkä koet tarpeelliseksi, jota ei ole vielä mainittu.',
    )

    is_attending_member = models.BooleanField(
        verbose_name='Olen Worldcon 75:n <em>attending member</em>'
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm
        return SignupExtraForm
