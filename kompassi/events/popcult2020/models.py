from django.db import models

from kompassi.labour.models import SignupExtraBase


class SignupExtra(SignupExtraBase):
    want_certificate = models.BooleanField(
        default=False,
        verbose_name="Haluan todistuksen työskentelystäni Popcult Helsingissä",
    )

    special_diet = models.ManyToManyField(
        "enrollment.SpecialDiet",
        blank=True,
        verbose_name="Erikoisruokavalio",
        related_name="%(app_label)s_%(class)s",
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

    y_u = models.TextField(
        blank=True,
        verbose_name="Miksi juuri sinä?",
        help_text=(
            "Miksi juuri sinä sopisit hakemaasi työtehtävään? Voit kertoa itsestäsi vapaamuotoisesti: "
            "harrastukset, koulutus, hullu-kissanainen/vähemmän-hullu-koiraihminen yms."
        ),
    )

    prior_experience = models.TextField(
        blank=True,
        verbose_name="Työkokemus",
        help_text=(
            "Kerro aikaisemmasta työkokemuksestasi tapahtuman työvoimana tai muusta kokemuksesta, "
            "josta koet olevan hyötyä haetussa/haetuissa työtehtävissä."
        ),
    )

    free_text = models.TextField(
        blank=True,
        verbose_name="Lisätietoja",
        help_text="Tässä kentässä voit kertoa jotain minkä koet tarpeelliseksi, jota ei ole vielä mainittu.",
    )

    @classmethod
    def get_form_class(cls):
        from .forms import SignupExtraForm

        return SignupExtraForm

    @classmethod
    def get_programme_form_class(cls):
        from .forms import ProgrammeSignupExtraForm

        return ProgrammeSignupExtraForm
