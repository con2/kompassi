# encoding: utf-8

from django.db import models

from labour.models import ObsoleteSignupExtraBaseV1
from labour.querybuilder import QueryBuilder, add_prefix

from core.utils import validate_slug


SHIFT_TYPE_CHOICES = [
    (u'2h', '2 tunnin vuoroja'),
    (u'4h', '4 tunnin vuoroja'),
    (u'yli4h', 'Yli 4 tunnin vuoroja'),
]


TOTAL_WORK_CHOICES = [
    (u'8h', '8 tuntia'),
    (u'yli8h', 'Yli 8 tuntia'),
]


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
    name = models.CharField(max_length=63)

    def __unicode__(self):
        return self.name


class SignupExtra(ObsoleteSignupExtraBaseV1):
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

    shirt_size = models.CharField(
        null=True,
        blank=True,
        max_length=8,
        choices=SHIRT_SIZES,
        verbose_name=u'Paidan koko',
        help_text=u'Ajoissa ilmoittautuneet vänkärit saavat mahdollisesti maksuttoman työvoimapaidan. '
            u'Kokotaulukot: <a href="http://www.bc-collection.eu/uploads/sizes/TU004.jpg" '
            u'target="_blank">unisex-paita</a>, <a href="http://www.bc-collection.eu/uploads/sizes/TW040.jpg" '
            u'target="_blank">ladyfit-paita</a>',
    )

    dead_dog = models.BooleanField(
        default=False,
        verbose_name=u'Osallistun dead dogeihin',
        help_text=u'Dead dogit ovat heti tapahtuman jälkeen järjestettävät kestit kaikille täysikäisille työvoimaan kuuluville. Dead dogit järjestetään TKL:n bussireittien tavoitettavissa olevassa paikassa. Ilmoittautuminen ei ole sitova.',
    )

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

    @staticmethod
    def get_query_class():
        return Signupfinncon2016


class Signupfinncon2016(QueryBuilder):
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
    default_views = [
        "signup__person__first_name",
        "signup__person__surname",
        "signup__person__nick",
    ]
    view_groups = (
        (u"Henkilötiedot", add_prefix("signup__person__", (
            "surname", "first_name", "nick", "phone", "email", "birth_date"))),
        (u"Sisäiset", add_prefix("signup__", (
            "state", "job_categories_accepted__pk", "notes", "created_at", "updated_at"))),
        (u"Työvuorotoiveet", "signup__job_categories__pk", "shift_type", "total_work"),
        (u"Lisätiedot", "special_diet__pk", "special_diet_other",
            "prior_experience", "free_text"),
        (u"Tila", add_prefix("signup__time_", ("accepted", "finished", "complained", "cancelled",
                                              "rejected", "arrived", "work_accepted", "reprimanded",))),
    )
