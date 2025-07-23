from django.db import models

from kompassi.labour.models import SignupExtraBase

TOTAL_WORK_CHOICES = [
    ("8h", "8 tuntia"),
    ("10h", "10–12 tuntia"),
    ("yli12h", "Työn sankari! Yli 12 tuntia"),
]

SHIRT_SIZES = [
    ("NO_SHIRT", "Ei paitaa"),
    ("XS", "XS Unisex"),
    ("S", "S Unisex"),
    ("M", "M Unisex"),
    ("L", "L Unisex"),
    ("XL", "XL Unisex"),
    ("XXL", "XXL Unisex"),
    ("3XL", "XXXL Unisex"),
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


class Night(SimpleChoice):
    pass


class SignupExtra(SignupExtraBase):
    total_work = models.CharField(
        max_length=15,
        verbose_name="Toivottu kokonaistyömäärä",
        help_text="Kuinka paljon haluat tehdä töitä yhteensä tapahtuman aikana?",
        choices=TOTAL_WORK_CHOICES,
    )

    want_certificate = models.BooleanField(
        default=False,
        verbose_name="Haluan todistuksen työskentelystäni Nekoconissa",
    )

    afterparty_participation = models.BooleanField(
        default=False,
        verbose_name="Haluan osallistua kaatajaisiin sunnuntaina conin jälkeen",
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

    lodging_needs = models.ManyToManyField(
        Night,
        blank=True,
        verbose_name="Majoitustarve",
        help_text="Tarvitsetko majoitusta? Merkitse ne yöt, joille tarvitset majoituksen. Kerro vapaassa alueessa, mikäli toivot majoittuvasi luokassa, jossa on vain tyttöjä tai vain poikia.",
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

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm

    @property
    def formatted_lodging_needs(self):
        return "\n".join(
            "{night}: {need}".format(
                night=night.name,
                need="Tarvitsee lattiamajoitusta"
                if self.lodging_needs.filter(pk=night.pk).exists()
                else "Ei tarvetta lattiamajoitukselle",
            )
            for night in Night.objects.all()
        )
