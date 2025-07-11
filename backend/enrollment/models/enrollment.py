from __future__ import annotations

from datetime import timedelta

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from core.utils.cleanup import register_cleanup

STATE_CHOICES = [
    ("NEW", _("New")),
    ("ACCEPTED", _("Accepted")),
    ("REJECTED", _("Rejected")),
    ("CANCELLED", _("Cancelled")),
]

STATE_LABEL_CLASSES = dict(
    NEW="label-info",
    ACCEPTED="label-success",
    REJECTED="label-danger",
    CANCELLED="label-danger",
)


@register_cleanup(
    lambda qs: qs.filter(
        event__start_time__lt=now() - timedelta(days=30),
        state__in=["CANCELLED", "REJECTED"],
    ),
)
class Enrollment(models.Model):
    """
    Holds all the possible fields an enrollment instance may have
    """

    event = models.ForeignKey("core.event", on_delete=models.CASCADE)
    person = models.ForeignKey("core.person", on_delete=models.CASCADE)
    state = models.CharField(
        max_length=max(len(key) for (key, label) in STATE_CHOICES),
        choices=STATE_CHOICES,
        default="ACCEPTED",
        verbose_name=_("State"),
    )

    special_diet = models.ManyToManyField(
        "enrollment.SpecialDiet",
        blank=True,
        verbose_name=_("Diet"),
        related_name="enrollments",
    )

    special_diet_other = models.TextField(
        blank=True,
        verbose_name=_("Other diets"),
        help_text=_(
            "If you're on a diet that's not included in the list, "
            "please detail your diet here. Event organizer will try "
            "to take dietary needs into consideration, but all diets "
            "may not be catered for."
        ),
    )

    is_public = models.BooleanField(
        null=True,
        blank=False,
        verbose_name="Näkyminen osallistujalistassa",
        choices=[
            (True, "Sallin nimeni julkaisemisen osallistujalistassa"),
            (False, "Kiellän nimeni julkaisemisen osallistujalistassa"),
        ],
        help_text=(
            "Tästä tapahtumasta julkistetaan osallistujalista, jossa näkyvät niiden osallistujien nimet, "
            "jotka ovat antaneet siihen luvan. Nimesi näytetään valitsemassasi muodossa, jonka voit "
            'tarkistaa ja muuttaa <a href="/profile" target="_blank">profiilissasi</a>.'
        ),
    )

    concon_event_affiliation = models.CharField(
        max_length=512,
        blank=True,
        default="",
        verbose_name="Mitä tapahtumia edustat?",
        help_text=(
            "Mikäli edustat jotain tapahtumaorganisaatiota, voit kertoa siitä tässä. "
            "Conconiin ovat tervetulleita osallistumaan kaikki kiinnostuneet, eli minkään "
            "tapahtumaorganisaation edustaminen ei ole edellytys osallistumiselle. "
            "Jos annat julkaista nimesi osallistujalistassa, myös tämä kenttä näytetään siinä."
        ),
    )

    concon_parts = models.ManyToManyField(
        "enrollment.ConconPart",
        blank=True,
        verbose_name="Mihin osiin tilaisuudesta osallistut?",
        help_text="Concon koostuu päivän luento- ja keskusteluohjelmasta sekä jatkosaunasta illalla.",
    )

    personal_identification_number = models.CharField(
        max_length=12,
        verbose_name="Henkilötunnus",
        help_text="Henkilötunnus luovutetaan kurssin järjestäjälle todistuksen kirjoittamista varten. Henkilötunnukset poistetaan tämän jälkeen järjestelmästä.",
        blank=True,
    )
    address = models.CharField(
        max_length=1023,
        blank=True,
        verbose_name="Katuosoite",
    )
    zip_code = models.CharField(
        max_length=5,
        blank=True,
        verbose_name="Postinumero",
    )
    city = models.CharField(
        max_length=127,
        blank=True,
        verbose_name="Postitoimipaikka",
    )

    traconjv_expiring = models.DateField(
        verbose_name="Milloin nykyinen JV-korttisi on umpeutumassa?",
        help_text="Päivämäärä muodossa 24.2.1994 tai 1994-02-24",
        blank=True,
        null=True,
    )
    traconjv_when = models.CharField(
        max_length=255, blank=True, verbose_name="Milloin olet käynyt järjestyksenvalvojan peruskoulutuksen?"
    )
    traconjv_avow_and_affirm = models.BooleanField(
        default=False,
        verbose_name="Vakuutan olevani lain tarkoittamalla tavalla rehellinen ja luotettava ja henkilökohtaisilta ominaisuuksiltani tehtävään sopiva, eikä minulla ole voimassaolevia tai vanhoja tuomioita tai rikosrekisteriä.",
    )
    traconjv_solemnly_swear = models.BooleanField(
        default=False,
        verbose_name="Vakuutan antamani tiedot oikeiksi. Sitoudun maksamaan kurssin hinnan täysimääräisenä, mikäli en pysty osallistumaan kurssille ja/tai järjestyksenvalvojana Tracon 2019 -tapahtumaan.",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def cancel(self):
        if self.state not in ("NEW", "ACCEPTED"):
            raise AssertionError(f"Can't cancel enrollment in state {self.state}")
        self.state = "CANCELLED"
        self.save()

    @property
    def is_active(self):
        return self.state == "ACCEPTED"

    @property
    def formatted_special_diet(self):
        return ", ".join(sd.name for sd in self.special_diet.all())

    def __str__(self):
        return f"{self.event}: {self.person}"

    @property
    def state_label_class(self):
        return STATE_LABEL_CLASSES.get(self.state, "label-default")

    def get_form_field_values(self):
        FormClass = self.event.enrollment_event_meta.form_class
        values = []
        # FIXME hideous hack
        for field_name in FormClass._meta.fields:
            getter = f"get_{field_name}_display"
            if hasattr(self, getter):
                values.append(getattr(self, getter)())
            else:
                values.append(getattr(self, field_name))
        return values

    @classmethod
    def get_form_field_header(cls, field_name):
        try:
            field = next(field for field in cls._meta.fields if field.name == field_name)
        except StopIteration:
            field = next(field for field in cls._meta.many_to_many if field.name == field_name)

        return field.verbose_name
