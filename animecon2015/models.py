# encoding: utf-8

from django.db import models

from labour.models import SignupExtraBase
from labour.querybuilder import QueryBuilder, add_prefix

from core.utils import validate_slug


SHIFT_TYPE_CHOICES = [
    (u'yksipitka', 'Yksi pitkä vuoro'),
    (u'montalyhytta', 'Monta lyhyempää vuoroa'),
    (u'kaikkikay', 'Kumpi tahansa käy'),
]

TOTAL_WORK_CHOICES = [
    (u'10h', '10 tuntia'),
    (u'12h', '12 tuntia'),
    (u'yli12h', 'Yli 12 tuntia'),
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

    personal_identification_number = models.CharField(
        max_length=12,
        verbose_name=u'Henkilötunnus',
        help_text=u'HUOM! Täytä tämä kenttä vain, jos haet <strong>kortittomaksi järjestyksenvalvojaksi</strong>.',
        default=u'',
        blank=True,
    )

    want_certificate = models.BooleanField(
        default=False,
        verbose_name=u'Haluan todistuksen työskentelystäni Animeconissa',
    )

    certificate_delivery_address = models.TextField(
        blank=True,
        verbose_name=u'Työtodistuksen toimitusosoite',
        help_text=u'Jos haluat työtodistuksen, täytä tähän kenttään postiosoite (katuosoite, '
            u'postinumero ja postitoimipaikka) johon haluat todistuksen toimitettavan.',
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
        return SignupAnimecon2015

    @property
    def formatted_lodging_needs(self):
        return u"\n".join(u"{night}: {need}".format(
            night=night.name,
            need=u'Tarvitsee lattiamajoitusta' if self.lodging_needs.filter(pk=night.pk).exists() else u'Ei tarvetta lattiamajoitukselle',
        ) for night in Night.objects.all())


class SignupAnimecon2015(QueryBuilder):
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
        (u"Työvuorotoiveet", "signup__job_categories__pk", "signup__work_periods__pk",
            "shift_type", "total_work", "construction", "overseer"),
        (u"Työtodistus", "want_certificate", "certificate_delivery_address"),
        (u"Lisätiedot", "special_diet__pk", "special_diet_other",
            "lodging_needs__pk", "prior_experience", "free_text"),
        (u"Tila", add_prefix("signup__time_", ("accepted", "finished", "complained", "cancelled",
                                              "rejected", "arrived", "work_accepted", "reprimanded",))),
    )
