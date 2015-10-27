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
    (u'8h', 'Minimi - 8 tuntia'),
    (u'12h', '10–12 tuntia'),
    (u'yli12h', 'Työn Sankari! Yli 12 tuntia!'),
]


class SimpleChoice(models.Model):
    name = models.CharField(max_length=63)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class SpecialDiet(SimpleChoice):
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

    want_certificate = models.BooleanField(
        default=False,
        verbose_name=u'Haluan todistuksen työskentelystäni Aiconissa',
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

    need_lodging = models.BooleanField(
        default=False,
        verbose_name=u'Tarvitsen lattiamajoitusta lauantain ja sunnuntain väliseksi yöksi',
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

    email_alias = models.CharField(
        blank=True,
        default=u'',
        max_length=32,
        verbose_name=u'Sähköpostialias',
        help_text=u'Vastaavat saavat käyttöönsä sähköpostialiakset, jotka ovat muotoa tehtävä@aicon.fi. '
            u'Mikäli tiedät jo Aiconin vastaavatehtäväsi, syötä se tähän mahdollisimman yksinkertaisessa muodossa (esim. pj, työvoima, ohjelma ym). '
            u'Osoitteessa isot kirjaimet muutetaan automaattisesti pieniksi, ä a:ksi ja niin edelleen. Näet lopullisen osoitteesi '
            u'<a href="/profile/aliases" target="_blank">profiilin sähköpostialiassivulta</a> sitten, '
            u'kun vastaavailmoittautumisesi on hyväksytty. Mikäli osoitteisiin tarvitaan tämän jälkeen muutoksia, Japsu auttaa.',
        validators=[validate_slug]
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm
        return SignupExtraForm

    @staticmethod
    def get_query_class():
        raise NotImplementedError()
