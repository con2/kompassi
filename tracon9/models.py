# encoding: utf-8

from django.db import models

from labour.models import SignupExtraBase


SHIRT_SIZES = [
    (u'NO_SHIRT', u'Ei paitaa'),

    (u'XS', u'XS Unisex'),
    (u'S', u'S Unisex'),
    (u'M', u'M Unisex'),
    (u'L', u'L Unisex'),
    (u'XL', u'XL Unisex'),
    (u'XXL', u'XXL Unisex'),
    (u'3XL', u'3XL Unisex'),
    (u'4XL', u'4XL Unisex'),
    (u'5XL', u'5XL Unisex'),

    (u'LF_XS', u'XS Ladyfit'),
    (u'LF_S', u'S Ladyfit'),
    (u'LF_M', u'M Ladyfit'),
    (u'LF_L', u'L Ladyfit'),
    (u'LF_XL', u'XL Ladyfit'),
]


class SpecialDiet(models.Model):
    name = models.CharField(max_length=31)

    def __unicode__(self):
        return self.name


class SignupExtra(SignupExtraBase):
    want_certificate = models.BooleanField(
        default=False,
        verbose_name=u'Haluan todistuksen työskentelystäni Traconissa',
    )

    certificate_delivery_address = models.TextField(
        blank=True,
        verbose_name=u'Työtodistuksen toimitusosoite',
        help_text=u'Jos haluat työtodistuksen, täytä tähän kenttään postiosoite (katuosoite, '
            u'postinumero ja postitoimipaikka) johon haluat todistuksen toimitettavan.',
    )

    shirt_size = models.CharField(max_length=8, choices=SHIRT_SIZES, verbose_name=u'Paidan koko')

    special_diet = models.ManyToManyField(
        SpecialDiet,
        blank=True,
        verbose_name=u'Erikoisruokavalio'
    )

    special_diet_other = models.TextField(
        blank=True,
        verbose_name=u'Muu erikoisruokavalio',
        help_text=u'Jos noudatat erikoisruokavaliota, jota ei ole yllä olevassa listassa, '
            u'ilmoita se tässä. Tapahtuman järjestäjä pyrkii ottamaan erikoisruokavaliot '
            u'huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään.'
    )

    prior_experience = models.TextField(
        blank=True,
        verbose_name=u'Työkokemus',
        help_text=u'Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista '
            u'tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä '
            u'hakemassasi tehtävässä.'
    )

    free_text = models.TextField(
        blank=True,
        verbose_name=u'Vapaa alue',
        help_text=u'Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole '
            u'omaa kenttää yllä, käytä tätä kenttää.'
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm
        return SignupExtraForm
