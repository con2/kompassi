# encoding: utf-8

from django.db import models

from labour.models import SignupExtraBase
from labour.querybuilder import QueryBuilder, add_prefix

from core.utils import validate_slug


SHIFT_TYPE_CHOICES = [
    (u'none', u'Ei väliä'),
    (u'4h', u'Pari pitkää vuoroa'),
    (u'yli4h', u'Useita lyhyitä vuoroja'),
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

SHIRT_TYPES = [
    (u'STAFF', u'Staff'),
    (u'DESURITY', u'Desurity'),
    (u'KUVAAJA', u'Kuvaaja'),
    (u'VENDOR', u'Myynti'),
    (u'TOOLATE', u'Myöhästyi paitatilauksesta'),
]


class SignupExtra(SignupExtraBase):
    shift_type = models.CharField(
        max_length=15,
        verbose_name=u'Toivottu työvuoron pituus',
        help_text=u'Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?',
        choices=SHIFT_TYPE_CHOICES,
    )

    desu_amount = models.PositiveIntegerField(
        verbose_name=u'Desumäärä',
        help_text=u'Kuinka monessa Desuconissa olet ollut vänkärinä?',
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
                  u'Jos haet valokuvaajaksi, kerro lisäksi millaista kuvauskalustoa sinulla on käytettävissäsi ja listaa'
                  u'muutamia gallerialinkkejä, joista pääsemme ihailemaan ottamiasi kuvia.'
    )

    shirt_size = models.CharField(
        max_length=8,
        choices=SHIRT_SIZES,
        default=u'NO_SHIRT',
        verbose_name=u'Paidan koko',
        help_text=u'Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan. '
                  u'Kokotaulukot: <a href="http://www.bc-collection.eu/uploads/sizes/TU004.jpg" '
                  u'target="_blank">unisex-paita</a>, <a href="http://www.bc-collection.eu/uploads/sizes/TW040.jpg" '
                  u'target="_blank">ladyfit-paita</a>',
    )

    shirt_type = models.CharField(
        max_length=8,
        choices=SHIRT_TYPES,
        default=u'TOOLATE',
        verbose_name=u'Paidan tyyppi',
    )

    night_work = models.BooleanField(
        verbose_name=u'Olen valmis tekemään yötöitä',
        default=False,
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm
        return SignupExtraForm

    @staticmethod
    def get_query_class():
        return Signupfrostbite2016


class Signupfrostbite2016(QueryBuilder):
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
        (u"Työvuorotoiveet", "signup__job_categories__pk", "shift_type",),
        (u"Lisätiedot", "shirt_size", "shirt_type", "desu_amount", "prior_experience", "free_text"),
        (u"Tila", add_prefix("signup__time_", ("accepted", "finished", "complained", "cancelled",
                                              "rejected", "arrived", "work_accepted", "reprimanded",))),
    )
