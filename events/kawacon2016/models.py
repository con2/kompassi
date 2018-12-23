from django.db import models

from core.utils import validate_slug
from labour.models import ObsoleteSignupExtraBaseV1


SHIRT_SIZES = [
    ('NO_SHIRT', 'Ei paitaa'),

    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),

    # (u'3XL', u'3XL'),
    # (u'4XL', u'4XL'),
    # (u'5XL', u'5XL'),

    # (u'LF_XS', u'XS Ladyfit'),
    # (u'LF_S', u'S Ladyfit'),
    # (u'LF_M', u'M Ladyfit'),
    # (u'LF_L', u'L Ladyfit'),
    # (u'LF_XL', u'XL Ladyfit'),
]


class SimpleChoice(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Night(SimpleChoice):
    pass


class SpecialDiet(SimpleChoice):
    pass


class SignupExtra(ObsoleteSignupExtraBaseV1):
    shirt_size = models.CharField(
        max_length=8,
        choices=SHIRT_SIZES,
        verbose_name='Paidan koko',
        help_text='Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan. '
            'Kokotaulukot: <a href="http://www.bc-collection.eu/uploads/sizes/TU004.jpg" '
            'target="_blank">unisex-paita</a>, <a href="http://www.bc-collection.eu/uploads/sizes/TW040.jpg" '
            'target="_blank">ladyfit-paita</a>',
    )

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

    needs_lodging = models.ManyToManyField(
        Night,
        blank=True,
        verbose_name='Majoitustarve lattiamajoituksessa',
        help_text='Vänkärinä saat tarvittaessa maksuttoman majoituksen lattiamajoituksessa. Merkitse tähän, minä öinä tarvitset lattiamajoitusta.',
    )

    prior_experience = models.TextField(
        blank=True,
        verbose_name='Työkokemus',
        help_text='Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista '
            'tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä '
            'hakemassasi tehtävässä.'
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
