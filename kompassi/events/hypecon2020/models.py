from django.db import models

from kompassi.labour.models import SignupExtraBase

SHIFT_TYPE_CHOICES = [
    ("yksipitka", "Yksi pitkä vuoro"),
    ("kaksilyhytta", "Kaksi lyhyempää vuoroa"),
    ("kaikkikay", "Kumpi tahansa käy"),
]

TOTAL_WORK_CHOICES = [
    ("3h", "3 tuntia"),
    ("4h", "4 tuntia"),
    ("5h", "5 tuntia"),
    ("xx", "Enemmän!"),
]

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
    ("LF_XS", "XS Ladyfit"),
    ("LF_S", "S Ladyfit"),
    ("LF_M", "M Ladyfit"),
    ("LF_L", "L Ladyfit"),
    ("LF_XL", "XL Ladyfit"),
    ("LF_XXL", "XXL Ladyfit"),
]


class SimpleChoice(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SpecialDiet(SimpleChoice):
    pass


class SignupExtra(SignupExtraBase):
    # want_certificate = models.BooleanField(
    #     default=False,
    #     verbose_name='Haluan todistuksen työskentelystäni Hypeconissa',
    # )

    shift_type = models.CharField(
        max_length=max(len(k) for (k, v) in SHIFT_TYPE_CHOICES),
        verbose_name="Toivottu työvuoron pituus",
        help_text="Haluatko tehdä yhden pitkän työvuoron vaiko monta lyhyempää vuoroa?",
        choices=SHIFT_TYPE_CHOICES,
    )

    total_work = models.CharField(
        max_length=max(len(k) for (k, v) in TOTAL_WORK_CHOICES),
        verbose_name="Toivottu kokonaistyömäärä",
        help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana?",
        choices=TOTAL_WORK_CHOICES,
    )

    shirt_size = models.CharField(
        max_length=8,
        choices=SHIRT_SIZES,
        verbose_name="Paidan koko",
        help_text="Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan.",
        default="NO_SHIRT",
    )

    special_diet = models.ManyToManyField(SpecialDiet, blank=True, verbose_name="Erikoisruokavalio")

    special_diet_other = models.TextField(
        blank=True,
        verbose_name="Muu erikoisruokavalio",
        help_text="Jos noudatat erikoisruokavaliota, jota ei ole yllä olevassa listassa, "
        "ilmoita se tässä. Tapahtuman järjestäjä pyrkii ottamaan erikoisruokavaliot "
        "huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään.",
    )

    free_text = models.TextField(
        blank=True,
        verbose_name="Miksi haluat vänkäriksi Hypeconiin?",
        help_text="Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole "
        "omaa kenttää yllä, käytä tätä kenttää.",
    )

    shift_wishes = models.TextField(
        blank=True,
        verbose_name="Alustavat työvuorotoiveet",
        help_text="Jos tiedät nyt jo, ettet pääse paikalle johonkin tiettyyn aikaan tai haluat "
        "osallistua johonkin tiettyyn ohjelmanumeroon, mainitse siitä tässä.",
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm

    @classmethod
    def get_programme_form_class(cls):
        from .forms import ProgrammeSignupExtraForm

        return ProgrammeSignupExtraForm
