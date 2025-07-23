from django.db import models

from kompassi.labour.models import SignupExtraBase

NIGHT_WORK_CHOICES = [
    ("miel", "Työskentelen mielelläni yövuorossa"),
    ("tarv", "Voin tarvittaessa työskennellä yövuorossa"),
    ("ei", "En vaan voi työskennellä yövuorossa"),
]

SHIFT_TYPE_CHOICES = [
    ("yksipitka", "Yksi pitkä vuoro"),
    ("montalyhytta", "Monta lyhyempää vuoroa"),
    ("kaikkikay", "Kumpi tahansa käy"),
]

TOTAL_WORK_CHOICES = [
    ("6h", "Minimi – 6 tuntia"),
    ("12h", "10–12 tuntia"),
    ("yli12h", "Työn Sankari! Yli 12 tuntia!"),
]

SHIRT_SIZES = [
    ("NO_SHIRT", "Ei paitaa"),
    ("BEANIE", "Pipo"),
    ("XS", "Paita – XS Unisex"),
    ("S", "Paita – S Unisex"),
    ("M", "Paita – M Unisex"),
    ("L", "Paita – L Unisex"),
    ("XL", "Paita – XL Unisex"),
    ("XXL", "Paita – XXL Unisex"),
    ("3XL", "Paita – 3XL Unisex"),
    ("4XL", "Paita – 4XL Unisex"),
    ("5XL", "Paita – 5XL Unisex"),
    ("LF_S", "Paita – S Ladyfit"),
    ("LF_M", "Paita – M Ladyfit"),
    ("LF_L", "Paita – L Ladyfit"),
    ("LF_XL", "Paita – XL Ladyfit"),
]


class SimpleChoice(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SpecialDiet(SimpleChoice):
    pass


class TimeSlot(SimpleChoice):
    pass


class SignupExtra(SignupExtraBase):
    shift_type = models.CharField(
        max_length=15,
        verbose_name="Toivottu työvuoron pituus",
        help_text="Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?",
        choices=SHIFT_TYPE_CHOICES,
    )

    total_work = models.CharField(
        max_length=15,
        verbose_name="Toivottu kokonaistyömäärä",
        help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana? Minimi on 6 tuntia.",
        choices=TOTAL_WORK_CHOICES,
    )

    night_work = models.CharField(
        max_length=5,
        verbose_name="Voitko työskennellä yöllä?",
        help_text="Yötöitä voi olla ainoastaan lauantain ja sunnuntain välisenä yönä.",
        choices=NIGHT_WORK_CHOICES,
    )

    construction = models.BooleanField(
        default=False,
        verbose_name="Voin työskennellä jo perjantaina",
        help_text="Huomaathan, että perjantain ja lauantain väliselle yölle ei ole tarjolla majoitusta.",
    )

    want_certificate = models.BooleanField(
        default=False,
        verbose_name="Haluan todistuksen työskentelystäni Hitpointissa",
    )

    certificate_delivery_address = models.TextField(
        blank=True,
        verbose_name="Työtodistuksen toimitusosoite",
        help_text="Jos haluat työtodistuksen, täytä tähän kenttään postiosoite (katuosoite, "
        "postinumero ja postitoimipaikka) johon haluat todistuksen toimitettavan.",
    )

    shirt_size = models.CharField(
        max_length=8,
        choices=SHIRT_SIZES,
        default="NO_SHIRT",
        verbose_name="Swägivalinta",
        help_text=(
            "Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan tai pipon. "
            "Valitse tässä, haluatko pipon vai paidan, ja paidan tapauksessa myös paidan koko. "
            'Kokotaulukot: <a href="https://dc-collection.fi/product/TU03T" '
            'target="_blank" rel="noopener noreferrer">unisex-paita</a>, <a href="https://dc-collection.fi/product/TW04T" '
            'target="_blank" rel="noopener noreferrer">ladyfit-paita</a>'
        ),
    )

    special_diet = models.ManyToManyField(SpecialDiet, blank=True, verbose_name="Erikoisruokavalio")

    special_diet_other = models.TextField(
        blank=True,
        verbose_name="Muu erikoisruokavalio",
        help_text="Jos noudatat erikoisruokavaliota, jota ei ole yllä olevassa listassa, "
        "ilmoita se tässä. Tapahtuman järjestäjä pyrkii ottamaan erikoisruokavaliot "
        "huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään.",
    )

    need_lodging = models.BooleanField(
        default=False,
        verbose_name="Tarvitsen lattiamajoitusta lauantain ja sunnuntain väliseksi yöksi",
    )

    prior_experience = models.TextField(
        blank=True,
        verbose_name="Työkokemus",
        help_text="Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista "
        "tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä "
        "hakemassasi tehtävässä.",
    )

    shift_wishes = models.TextField(
        blank=True,
        verbose_name="Alustavat työvuorotoiveet",
        help_text="Jos tiedät nyt jo, ettet pääse paikalle johonkin tiettyyn aikaan tai haluat "
        "osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siitä tässä.",
    )

    free_text = models.TextField(
        blank=True,
        verbose_name="Vapaa alue",
        help_text="Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole "
        "omaa kenttää yllä, käytä tätä kenttää.",
    )

    afterparty_participation = models.BooleanField(
        default=False,
        verbose_name="Osallistun kaatajaisiin",
        help_text=(
            "Ruksaa tämä ruutu, mikäli haluat osallistua kaatajaisiin. Mikäli mielesi muuttuu "
            "tai sinulle tulee este, peru ilmoittautumisesi poistamalla rasti tästä ruudusta. "
        ),
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm

    @classmethod
    def get_programme_form_class(cls):
        from .forms import ProgrammeSignupExtraForm

        return ProgrammeSignupExtraForm
