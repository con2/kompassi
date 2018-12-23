# encoding: utf-8



from django.db import models

from labour.models import SignupExtraBase

from core.utils import validate_slug


SHIRT_SIZES = [
    ('NO_SHIRT', 'Ei paitaa'),

    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
    ('3XL', '3XL'),

    # ('4XL', '4XL'),
    # ('5XL', '5XL'),

    # ('LF_XS', 'XS Ladyfit'),
    # ('LF_S', 'S Ladyfit'),
    # ('LF_M', 'M Ladyfit'),
    # ('LF_L', 'L Ladyfit'),
    # ('LF_XL', 'XL Ladyfit'),
]

AFTERPARTY_CHOICES = [
    ('joo', 'Kyllä'),
    ('ei', 'Ei'),
    ('ehk', 'Kyllä, jos majoitus ja/tai kyyti järjestyy'),
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


class Shift(SimpleChoice):
    pass



class SignupExtra(SignupExtraBase):
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

    shifts = models.ManyToManyField(
        Shift,
        verbose_name='Voin työskennellä',
        help_text='Milloin olet käytettävissä? Tilavänkäreille (ja muille halukkaille) on tarjolla työvuoroja myös ennen conin aukeamista sekä conin päättymisen jälkeen.',
    )

    afterparty = models.CharField(
        max_length=max(len(key) for (key, text) in AFTERPARTY_CHOICES),
        choices=AFTERPARTY_CHOICES,
        verbose_name='Haluatko osallistua kaatajaisiin sunnutai-iltana?',
        help_text='Conin jälkeen järjestetään työvoiman päätösjuhla sunnuntai-iltana. Kerro tässä jos haluat osallistua.',
    )

    want_certificate = models.BooleanField(
        default=False,
        verbose_name='Haluan työtodistuksen työskentelystäni Kawaconissa',
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

    @classmethod
    def get_programme_form_class(cls):
        from .forms import ProgrammeSignupExtraForm
        return ProgrammeSignupExtraForm
