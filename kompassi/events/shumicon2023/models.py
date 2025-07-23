from django.db import models

from kompassi.labour.models import SignupExtraBase

SHIRT_SIZES = [
    ("NO_SHIRT", "Ei paitaa"),
    ("XS", "XS Unisex"),
    ("S", "S Unisex"),
    ("M", "M Unisex"),
    ("L", "L Unisex"),
    ("XL", "XL Unisex"),
    ("XXL", "XXL Unisex"),
    ("3XL", "3XL Unisex"),
    ("4XL", "4XL Unisex"),
    ("5XL", "5XL Unisex"),
    # (u'LF_XS', u'XS Ladyfit'),
    # (u'LF_S', u'S Ladyfit'),
    # (u'LF_M', u'M Ladyfit'),
    # (u'LF_L', u'L Ladyfit'),
    # (u'LF_XL', u'XL Ladyfit'),
]

SHIFT_TYPE_CHOICES = [
    ("yksipitka", "Yksi pitkä vuoro"),
    ("montalyhytta", "Monta lyhyempää vuoroa"),
    ("kaikkikay", "Kumpi tahansa käy"),
]

TOTAL_WORK_CHOICES = [
    ("8h", "Minimi - 8 tuntia"),
    ("10h", "8-10 tuntia"),
    ("yli10h", "Työn Sankari! Yli 10 tuntia!"),
]

BUILD_PARTICIPATION_CHOICES = [
    ("ei", "En pysty osallistumaan kumpaankaan"),
    ("kasaus", "Pystyn osallistumaan vain kasaukseen"),
    ("purku", "Pystyn osallistumaan vain purkuun"),
    ("molemmat", "Pystyn osallistumaan molempiin"),
]


class SimpleChoice(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SpecialDiet(SimpleChoice):
    pass


class EventDay(SimpleChoice):
    pass


class NativeLanguage(SimpleChoice):
    pass


class KnownLanguage(SimpleChoice):
    pass


class SignupExtra(SignupExtraBase):
    shift_type = models.CharField(
        max_length=15,
        verbose_name="Toivottu työvuoron pituus",
        help_text="Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?",
        choices=SHIFT_TYPE_CHOICES,
    )

    shift_leader = models.BooleanField(
        default=False,
        verbose_name="Oletko kiinnostunut vuorovastaavan tehtävistä? Vuorovastaava koordinoi vuoron aikana tehtäviä ja tauotuksia.",
    )

    total_work = models.CharField(
        max_length=15,
        verbose_name="Toivottu kokonaistyömäärä",
        help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana?",
        choices=TOTAL_WORK_CHOICES,
    )

    build_participation = models.CharField(
        max_length=15,
        verbose_name="Kasaus ja purku",
        help_text="Valitse pystytkö osallistumaan kasaukseen ja/tai purkuun",
        choices=BUILD_PARTICIPATION_CHOICES,
    )

    work_days = models.ManyToManyField(
        EventDay,
        verbose_name="Tapahtumapäivät",
        help_text="Minä päivinä olet halukas työskentelemään?",
    )

    shirt_size = models.CharField(
        max_length=8,
        choices=SHIRT_SIZES,
        verbose_name="Paidan koko",
        help_text="Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan.",
        default="NO_SHIRT",
    )

    native_language = models.ManyToManyField(
        NativeLanguage,
        verbose_name="Äidinkielesi",
    )
    native_language_other = models.TextField(
        blank=True,
        verbose_name="Muu äidinkieli",
    )

    known_language = models.ManyToManyField(
        KnownLanguage,
        blank=True,
        verbose_name="Muut osaamasi kielet",
    )
    known_language_other = models.TextField(
        blank=True,
        verbose_name="Muu osaamasi kieli",
    )

    special_diet = models.ManyToManyField(SpecialDiet, blank=True, verbose_name="Erikoisruokavalio")

    special_diet_other = models.TextField(
        blank=True,
        verbose_name="Muu erikoisruokavalio",
        help_text="Jos noudatat erikoisruokavaliota, jota ei ole yllä olevassa listassa, "
        "ilmoita se tässä. Tapahtuman järjestäjä pyrkii ottamaan erikoisruokavaliot "
        "huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään.",
    )

    shift_wishes = models.TextField(
        blank=True,
        verbose_name="Alustavat työvuorotoiveet",
        help_text="Jos tiedät nyt jo, ettet pääse paikalle johonkin tiettyyn aikaan tai haluat "
        "osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siitä tässä.",
    )

    # prior_experience = models.TextField(
    #     blank=True,
    #     verbose_name="Työkokemus",
    #     help_text="Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista "
    #     "tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä "
    #     "hakemassasi tehtävässä.",
    # )

    # free_text = models.TextField(
    #     blank=True,
    #     verbose_name="Vapaa alue",
    #     help_text="Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole "
    #     "omaa kenttää yllä, käytä tätä kenttää.",
    # )

    why_work = models.TextField(
        blank=True,
        verbose_name="Miksi haluaisit työskennellä Shumiconissa?",
        help_text="Kerro mikä Shumiconissa viehättää ja miksi haluaisit tulla juuri tähän tapahtumaan",
    )

    why_you = models.TextField(
        blank=True,
        verbose_name="Miksi olisit hyvä valinta hakemaasi työtehtävään?",
        help_text="Kerro miksi hait juuri kyseisiin tehtäviin ja miksi juuri sinut tulisi valita",
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm

    @classmethod
    def get_programme_form_class(cls):
        from .forms import ProgrammeSignupExtraForm

        return ProgrammeSignupExtraForm
