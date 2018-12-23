from django.db import models

from core.utils import validate_slug
from labour.models import ObsoleteSignupExtraBaseV1


TOTAL_WORK_CHOICES = [
    ('minimi', 'Haluan tehdä vain minimityöpanoksen (JV: 10h, muut: 8h)'),
    ('ekstra', 'Olen valmis tekemään lisätunteja'),
]

KORTITON_JV_HETU_LABEL = 'Henkilötunnus'
KORTITON_JV_HETU_HELP_TEXT = 'HUOM! Täytä tämä kenttä vain, jos haet <strong>kortittomaksi järjestyksenvalvojaksi</strong>.'


class SimpleChoice(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SpecialDiet(SimpleChoice):
    pass


class Night(SimpleChoice):
    pass


class SignupExtra(ObsoleteSignupExtraBaseV1):
    total_work = models.CharField(max_length=15,
        verbose_name='Toivottu kokonaistyömäärä',
        help_text='Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana?',
        choices=TOTAL_WORK_CHOICES,
    )

    personal_identification_number = models.CharField(
        max_length=12,
        verbose_name=KORTITON_JV_HETU_LABEL,
        help_text=KORTITON_JV_HETU_HELP_TEXT,
        default='',
        blank=True,
    )

    want_certificate = models.BooleanField(
        default=False,
        verbose_name='Haluan todistuksen työskentelystäni Animeconissa',
    )

    certificate_delivery_address = models.TextField(
        blank=True,
        verbose_name='Työtodistuksen toimitusosoite',
        help_text='Jos haluat työtodistuksen, täytä tähän kenttään postiosoite (katuosoite, '
            'postinumero ja postitoimipaikka) johon haluat todistuksen toimitettavan.',
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

    lodging_needs = models.ManyToManyField(Night,
        blank=True,
        verbose_name='Tarvitsen lattiamajoitusta',
        help_text='Ruksaa ne yöt, joille tarvitset lattiamajoitusta. Lattiamajoitus sijaitsee '
            'kävelymatkan päässä tapahtumapaikalta.',
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

    @property
    def formatted_lodging_needs(self):
        return "\n".join("{night}: {need}".format(
            night=night.name,
            need='Tarvitsee lattiamajoitusta' if self.lodging_needs.filter(pk=night.pk).exists() else 'Ei tarvetta lattiamajoitukselle',
        ) for night in Night.objects.all())
