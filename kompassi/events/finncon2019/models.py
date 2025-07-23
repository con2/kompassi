from django.db import models

from kompassi.labour.models import SignupExtraBase

SHIFT_TYPE_CHOICES = [
    ("2h", "2 tunnin vuoroja"),
    ("4h", "4 tunnin vuoroja"),
    ("yli4h", "Yli 4 tunnin vuoroja"),
]


TOTAL_WORK_CHOICES = [
    ("4h", "4–8 tuntia"),
    ("8h", "8 tuntia"),
    ("yli8h", "Yli 8 tuntia"),
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
    ("LF_2XL", "2XL Ladyfit"),
    ("LF_3XL", "3XL Ladyfit"),
]


class SpecialDiet(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


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
        help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana?",
        choices=TOTAL_WORK_CHOICES,
    )

    shirt_size = models.CharField(
        null=True,
        blank=True,
        max_length=8,
        choices=SHIRT_SIZES,
        verbose_name="Paidan koko",
        help_text=(
            "Ajoissa ilmoittautuneet vänkärit saavat maksuttoman työvoimapaidan, "
            "mikäli ilmoittavat työskentelevänsä vähintään 8 tuntia."
        ),
    )

    dead_dog = models.BooleanField(
        default=False,
        verbose_name="Osallistun dead dogeihin",
        help_text=(
            "Dead dogit ovat heti tapahtuman jälkeen järjestettävät kestit "
            "kaikille täysikäisille työvoimaan kuuluville. Ilmoittautuminen ei ole sitova."
        ),
    )

    special_diet = models.ManyToManyField(SpecialDiet, blank=True, verbose_name="Erikoisruokavalio")

    special_diet_other = models.TextField(
        blank=True,
        verbose_name="Muu erikoisruokavalio",
        help_text=(
            "Jos noudatat erikoisruokavaliota, jota ei ole yllä olevassa listassa, "
            "ilmoita se tässä. Tapahtuman järjestäjä pyrkii ottamaan erikoisruokavaliot "
            "huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään."
        ),
    )

    prior_experience = models.TextField(
        blank=True,
        verbose_name="Työkokemus",
        help_text=(
            "Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista "
            "tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä "
            "hakemassasi tehtävässä."
        ),
    )

    language_skills = models.TextField(
        blank=True,
        default="",
        verbose_name="Kielitaito",
        help_text="Kerro kielitaidostasi erityisesti suomen, ruotsin ja englannin kielissä.",
    )

    free_text = models.TextField(
        blank=True,
        verbose_name="Vapaa alue",
        help_text=(
            "Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole "
            "omaa kenttää yllä, käytä tätä kenttää."
        ),
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm
