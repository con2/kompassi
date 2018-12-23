from django.db import models

from core.utils import validate_slug
from labour.models import SignupExtraBase


SHIFT_TYPE_CHOICES = [
    ('yksipitka', 'Yksi pitkä vuoro'),
    ('montalyhytta', 'Monta lyhyttä vuoroa'),
    ('eivalia', 'Ei väliä'),
]


TOTAL_WORK_CHOICES = [
    ('8h', '8 tuntia'),
    ('12h', '12 tuntia'),
]


WORKING_DAYS_CHOICES = [
    ('pe', 'Perjantaina'),
    ('la', 'Lauantaina'),
    ('pela', 'Molempina päivinä'),
]


class SpecialDiet(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class SignupExtra(SignupExtraBase):
    special_diet = models.ManyToManyField(
        SpecialDiet,
        blank=True,
        verbose_name='Erikoisruokavalio'
    )

    special_diet_other = models.TextField(
        blank=True,
        verbose_name='Muu erikoisruokavalio',
        help_text='Jos noudatat erikoisruokavaliota, jota ei ole yllä olevassa listassa, '
            'ilmoita se tässä. Tapahtuman järjestäjä pyrkii ottamaan erikoisruokavaliot '
            'huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään.'
    )

    total_work = models.CharField(max_length=15,
        verbose_name='Maksimityömäärä',
        help_text='Kuinka paljon haluat enintään tehdä töitä yhteensä tapahtuman aikana?',
        choices=TOTAL_WORK_CHOICES,
    )

    shift_type = models.CharField(max_length=15,
        verbose_name='Toivottu työvuoron pituus',
        help_text='Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?',
        choices=SHIFT_TYPE_CHOICES,
    )

    working_days = models.CharField(
        verbose_name='Työskenteleminen tapahtumassa',
        help_text='Vänkärinä voit ottaa työvuoroja perjantaina, lauantaina tai molempina päivinä.',
        max_length=4,
        choices=WORKING_DAYS_CHOICES,
    )

    prior_experience = models.TextField(
        blank=True,
        verbose_name='Työkokemus',
        help_text='Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista '
            'tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä '
            'hakemassasi tehtävässä.'
    )

    shift_wishes = models.TextField(
        blank=True,
        verbose_name='Alustavat työvuorotoiveet',
        help_text='Jos tiedät nyt jo, ettet pääse paikalle johonkin tiettyyn aikaan tai haluat '
            'osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siitä tässä.'
    )

    free_text = models.TextField(
        blank=True,
        verbose_name='Vapaa alue',
        help_text='Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole '
            'omaa kenttää yllä, käytä tätä kenttää.'
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm
        return SignupExtraForm
