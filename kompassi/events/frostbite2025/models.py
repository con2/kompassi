from django.db import models

from kompassi.labour.models import SignupExtraBase

SHIFT_TYPE_CHOICES = [
    ("none", "Ei väliä"),
    ("4h", "Pari pitkää vuoroa"),
    ("yli4h", "Useita lyhyitä vuoroja"),
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
]

SHIRT_TYPES = [
    ("NO_SHIRT", "Ei paitaa"),
    ("STAFF", "Staff"),
    ("DESURITY", "Desurity"),
    ("DESUTV", "DesuTV"),
    ("KUVAAJA", "Kuvaaja"),
    ("VENDOR", "Myynti"),
    ("TOOLATE", "Myöhästyi paitatilauksesta"),
]

ACCOMMODATION_CHOICES = [
    ("no_need", "En majoitu Kuusessa"),
    ("pe_la", "Majoitun pe-la"),
    ("la_su", "Majoitun la-su"),
    ("whole_weekend", "Majoitun koko viikonlopun"),
]


class SpecialDiet(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Poison(models.Model):
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

    prior_experience = models.TextField(
        blank=True,
        verbose_name="Työkokemus",
        help_text=(
            "Kerro tässä kentässä, jos sinulla on aiempaa kokemusta vastaavista "
            "tehtävistä tai muuta sellaista työkokemusta, josta arvioit olevan hyötyä "
            "hakemassasi tehtävässä."
        ),
    )

    free_text = models.TextField(
        blank=True,
        verbose_name="Vapaa alue",
        help_text=(
            "Jos haluat sanoa hakemuksesi käsittelijöille jotain sellaista, jolle ei ole "
            "omaa kenttää yllä, käytä tätä kenttää. "
        ),
    )

    special_diet = models.ManyToManyField(
        SpecialDiet,
        blank=True,
        verbose_name="Erikoisruokavalio",
        related_name="_frostbite2025_signupextra_special_diet+",
    )

    special_diet_other = models.TextField(
        blank=True,
        verbose_name="Muu erikoisruokavalio",
        help_text=(
            "Jos noudatat erikoisruokavaliota, jota ei ole yllä olevassa listassa, "
            "ilmoita se tässä. Tapahtuman järjestäjä pyrkii ottamaan erikoisruokavaliot "
            "huomioon, mutta kaikkia erikoisruokavalioita ei välttämättä pystytä järjestämään."
        ),
    )

    shirt_size = models.CharField(
        max_length=8,
        choices=SHIRT_SIZES,
        default="NO_SHIRT",
        verbose_name="Paidan koko",
        help_text=(
            "Ajoissa ilmoittautuneet saavat maksuttoman työvoimapaidan. "
            'Kokotaulukot: <a href="https://dc-collection.fi/product/TU03T" '
            'target="_blank" rel="noopener noreferrer">unisex-paita</a>, <a href="https://dc-collection.fi/product/TW04T" '
            'target="_blank" rel="noopener noreferrer">ladyfit-paita</a>'
        ),
    )

    shirt_type = models.CharField(
        max_length=8,
        choices=SHIRT_TYPES,
        default="TOOLATE",
        verbose_name="Paidan tyyppi",
    )

    night_work = models.BooleanField(
        verbose_name="Olen valmis tekemään yötöitä",
        default=False,
    )

    afterparty_participation = models.BooleanField(
        default=False,
        verbose_name="Osallistun kaatajaisiin",
        help_text=(
            "Ruksaa tämä ruutu, mikäli haluat osallistua kaatajaisiin. Mikäli mielesi muuttuu "
            "tai sinulle tulee este, peru ilmoittautumisesi poistamalla rasti tästä ruudusta."
        ),
    )

    accommodation = models.CharField(
        max_length=max(len(c) for (c, t) in ACCOMMODATION_CHOICES),
        choices=ACCOMMODATION_CHOICES,
        default=ACCOMMODATION_CHOICES[0][0],
        verbose_name="Työvoimamajoitus",
    )

    pick_your_poison = models.ManyToManyField(
        Poison,
        blank=True,
        verbose_name="Mitä haluaisit juoda kaatajaisissa?",
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm

    @classmethod
    def get_programme_form_class(cls):
        from .forms import ProgrammeSignupExtraForm

        return ProgrammeSignupExtraForm

    def get_shirt_size_display(self):
        """
        Emconsisten displayage of shirt type and size in onboarding view
        """
        if self.shirt_type == "NO_SHIRT":
            return "Ei paitaa"
        else:
            return next((name for (slug, name) in SHIRT_SIZES if slug == self.shirt_size), "")

    def get_shirt_type_display(self):
        """
        Emconsisten displayage of shirt type and size in onboarding view
        """
        if self.shirt_size == "NO_SHIRT":
            return "Ei paitaa"
        else:
            return next((name for (slug, name) in SHIRT_TYPES if slug == self.shirt_type), "")
