from django.db import models

from labour.models import SignupExtraBase


SHIRT_SIZES = [
    ('NO_SHIRT', 'En halua paitaa'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('OTHER', 'Muu koko (kerro Vapaa sana -kentässä)'),
]


class SignupExtra(SignupExtraBase):
    want_certificate = models.BooleanField(
        default=False,
        verbose_name='Haluan todistuksen työskentelystäni Matsuconissa',
    )

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
        ),
    )

    night_work = models.BooleanField(
        verbose_name='Olen valmis tekemään yötyötä (jos valitsit työn, joka sellaista sisältää)',
        default=False,
    )

    need_lodging = models.BooleanField(
        verbose_name='Tarvitsen majoituksen (lattiamajoitus)',
        default=False,
    )

    more_info = models.TextField(
        blank=True,
        default='',
        verbose_name='Lisätietoja osaamisestasi',
        help_text=(
            'Jos valitsit työn, joka tarvitsee selvennystä osaamisestasi (ensiapukortti, linkki '
            'portfolioon jne.), kirjoita siitä tähän.'
        )
    )

    prior_experience = models.TextField(
        blank=True,
        verbose_name='Työkokemus',
        help_text=(
            'Oletko tehnyt vastaavaa työtä aikaisemmin? Muuta hyödyllistä työkokemusta? Kerro itsestäsi!'
        ),
    )

    free_text = models.TextField(
        blank=True,
        verbose_name='Vapaa sana',
        help_text='Muuta kerrottavaa? Kysyttävää? Kirjoita se tähän.',
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm
        return SignupExtraForm

    @classmethod
    def get_programme_form_class(cls):
        from .forms import ProgrammeSignupExtraForm
        return ProgrammeSignupExtraForm

    @staticmethod
    def get_query_class():
        raise NotImplementedError()
