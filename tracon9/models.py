# encoding: utf-8

from django.db import models

from labour.models import SignupExtraBase
from labour.querybuilder import QueryBuilder


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

SHIFT_TYPE_CHOICES = [
    (u'yksipitka', 'Yksi pitkä vuoro'),
    (u'montalyhytta', 'Monta lyhyempää vuoroa'),
    (u'kaikkikay', 'Kumpi tahansa käy'),
]

TOTAL_WORK_CHOICES = [
    (u'8h', 'Minimi - 8 tuntia (1 lämmin ateria)'),
    (u'12h', '12 tuntia (2 lämmintä ateriaa)'),
    (u'yli12h', 'Työn Sankari! Yli 12 tuntia! (2 lämmintä ateriaa)'),
]


class SimpleChoice(models.Model):
    name = models.CharField(max_length=63)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class SpecialDiet(SimpleChoice):
    pass


class Night(SimpleChoice):
    pass


class SignupExtra(SignupExtraBase):
    shift_type = models.CharField(max_length=15,
        verbose_name=u'Toivottu työvuoron pituus',
        help_text=u'Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?',
        choices=SHIFT_TYPE_CHOICES,
    )

    total_work = models.CharField(max_length=15,
        verbose_name=u'Toivottu kokonaistyömäärä',
        help_text=u'Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Useimmissa tehtävistä minimi on kahdeksan tuntia, mutta joissain tehtävissä se voi olla myös vähemmän (esim. majoitusvalvonta 6 h).',
        choices=TOTAL_WORK_CHOICES,
    )

    construction = models.BooleanField(
        verbose_name=u'Voin osallistua perjantain kasaustalkoisiin',
        help_text=u'Kasaustalkoisiin osallistumista ei lasketa tapahtuman aikaiseen kokonaistyömäärään.',
    )

    overseer = models.BooleanField(
        verbose_name=u'Olen kiinnostunut vänkärikersantin tehtävistä',
        help_text=u'Ylivänkärit eli kersantit ovat kokeneempia conityöläisiä, jotka toimivat oman tehtäväalueensa tiiminvetäjänä.',
    )

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

    lodging_needs = models.ManyToManyField(Night,
        blank=True,
        verbose_name=u'Tarvitsen lattiamajoitusta',
        help_text=u'Ruksaa ne yöt, joille tarvitset lattiamajoitusta. Lattiamajoitus sijaitsee '
            u'kävelymatkan päässä tapahtumapaikalta.',
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

    @staticmethod
    def get_query_class():
        return Signup9


class Signup9(QueryBuilder):
    model = SignupExtra
    query_related_exclude = {
        "signup": ("event",),
    }
    query_related_filter = {
        "signup": "*",
        "signup__person": ("birth_date",),
    }
    view_related_filter = {
        "signup__person": ("first_name", "surname", "nick", "birth_date", "email", "phone",),
    }
