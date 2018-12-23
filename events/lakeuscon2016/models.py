# encoding: utf-8

from django.db import models

from labour.models import ObsoleteSignupExtraBaseV1


SHIRT_SIZES = [
    ('NO_SHIRT', 'Ei paitaa'),

    ('XS', 'XS Unisex'),
    ('S', 'S Unisex'),
    ('M', 'M Unisex'),
    ('L', 'L Unisex'),
    ('XL', 'XL Unisex'),
    ('XXL', 'XXL Unisex'),
    ('3XL', '3XL Unisex'),
    ('4XL', '4XL Unisex'),
    ('5XL', '5XL Unisex'),

    ('LF_XS', 'XS Ladyfit'),
    ('LF_S', 'S Ladyfit'),
    ('LF_M', 'M Ladyfit'),
    ('LF_L', 'L Ladyfit'),
    ('LF_XL', 'XL Ladyfit'),
]


SHIFT_TYPE_CHOICES = [
    ('yksipitka', 'Yksi pitkä vuoro'),
    ('montalyhytta', 'Monta lyhyempää vuoroa'),
    ('kaikkikay', 'Kumpi tahansa käy'),
]


class SpecialDiet(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class SignupExtra(ObsoleteSignupExtraBaseV1):
    shift_type = models.CharField(max_length=15,
        verbose_name='Toivottu työvuoron pituus',
        help_text='Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?',
        choices=SHIFT_TYPE_CHOICES,
    )

    # total_work = models.CharField(max_length=15,
    #     verbose_name=u'Toivottu kokonaistyömäärä',
    #     help_text=u'Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Useimmissa tehtävistä minimi on kahdeksan tuntia, mutta joissain tehtävissä se voi olla myös vähemmän (esim. majoitusvalvonta 6 h).',
    #     choices=TOTAL_WORK_CHOICES,
    # )

    shirt_size = models.CharField(
        max_length=8,
        choices=SHIRT_SIZES,
        verbose_name='Paidan koko',
        help_text='Ajoissa ilmoittautuneille pyritään hankkimaan työvoimapaidat. '
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

    # need_lodging = models.BooleanField(
    #     default=False,
    #     verbose_name=u'Tarvitsen lattiamajoitusta lauantain ja sunnuntain väliseksi yöksi',
    # )

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
