import logging
import typing
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import get_language, gettext_lazy as _

from ..utils import (
    format_date_range,
    pick_attrs,
    SLUG_FIELD_PARAMS,
    slugify,
    event_meta_property,
)

if typing.TYPE_CHECKING:
    from program_v2.models import Program, Dimension


logger = logging.getLogger("kompassi")


class Event(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)

    name = models.CharField(max_length=63, verbose_name="Tapahtuman nimi")

    organization = models.ForeignKey(
        "core.Organization", on_delete=models.CASCADE, verbose_name="Järjestäjätaho", related_name="events"
    )

    name_genitive = models.CharField(
        max_length=63,
        verbose_name="Tapahtuman nimi genetiivissä",
        help_text="Esimerkki: Susiconin",
    )

    name_illative = models.CharField(
        max_length=63,
        verbose_name="Tapahtuman nimi illatiivissä",
        help_text="Esimerkki: Susiconiin",
    )

    name_inessive = models.CharField(
        max_length=63,
        verbose_name="Tapahtuman nimi inessiivissä",
        help_text="Esimerkki: Susiconissa",
    )

    description = models.TextField(blank=True, verbose_name="Kuvaus")

    venue = models.ForeignKey(
        "core.Venue",
        on_delete=models.CASCADE,
        verbose_name="Tapahtumapaikka",
    )

    start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Alkamisaika",
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Päättymisaika",
    )

    homepage_url = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Tapahtuman kotisivu",
    )

    public = models.BooleanField(
        default=True, verbose_name="Julkinen", help_text="Julkiset tapahtumat näytetään etusivulla."
    )

    cancelled = models.BooleanField(
        default=False,
        verbose_name=_("Cancelled"),
    )

    logo_file = models.FileField(
        upload_to="event_logos",
        blank=True,
        verbose_name="Tapahtuman logo",
        help_text="Näkyy tapahtumasivulla. Jos sekä tämä että logon URL -kenttä on täytetty, käytetään tätä.",
    )

    logo_url = models.CharField(
        blank=True,
        max_length=255,
        default="",
        verbose_name="Tapahtuman logon URL",
        help_text="Voi olla paikallinen (alkaa /-merkillä) tai absoluuttinen (alkaa http/https)",
    )

    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Tapahtuman kuvaus",
        help_text="Muutaman kappaleen mittainen kuvaus tapahtumasta. Näkyy tapahtumasivulla.",
    )

    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    # related fields
    programs: models.QuerySet["Program"]
    dimensions: models.QuerySet["Dimension"]

    class Meta:
        verbose_name = "Tapahtuma"
        verbose_name_plural = "Tapahtumat"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            for field, suffix in [
                ("name_genitive", "in"),
                ("name_illative", "iin"),
                ("name_inessive", "issa"),
            ]:
                if not getattr(self, field, None):
                    setattr(self, field, self.name + suffix)

        return super().save(*args, **kwargs)

    @property
    def panel_css_class(self):
        return self.organization.panel_css_class

    @property
    def name_and_year(self):
        return f"{self.name} ({self.start_time.year})"

    @property
    def formatted_start_and_end_date(self):
        # TODO honor locale (currently always uses Finnish format)
        return format_date_range(self.start_time, self.end_time)

    @property
    def headline(self):
        """
        fi: Susikeskuksessa 1.–3.4.2016
        en: Susikeskus 1.–3.4.2016
        """
        headline_parts = []

        if self.venue:
            if get_language() == "fi":
                headline_parts.append(self.venue.name_inessive)
            else:
                headline_parts.append(self.venue.name)

        if self.start_time and self.end_time:
            headline_parts.append(self.formatted_start_and_end_date)

        return " ".join(headline_parts)

    @property
    def venue_name(self):
        return self.venue.name if self.venue else None

    @classmethod
    def get_or_create_dummy(cls, name="Dummy event"):
        from .venue import Venue
        from .organization import Organization

        # TODO not the best place for this, encap. see also admin command core_update_maysendinfo
        from django.contrib.auth.models import Group

        Group.objects.get_or_create(name=settings.KOMPASSI_MAY_SEND_INFO_GROUP_NAME)

        venue, unused = Venue.get_or_create_dummy()
        organization, unused = Organization.get_or_create_dummy()
        t = timezone.now()

        return cls.objects.get_or_create(
            name=name,
            defaults=dict(
                venue=venue,
                start_time=t + timedelta(days=60),
                end_time=t + timedelta(days=61),
                slug=slugify(name),
                organization=organization,
            ),
        )

    @property
    def people(self):
        """
        Returns people associated with this event
        """
        from .person import Person

        # have signups
        q = Q(signups__event=self)

        # or programmes
        q |= Q(programme_roles__programme__category__event=self)

        return Person.objects.filter(q).distinct()

    @property
    def either_logo_url(self):
        if self.logo_file:
            return self.logo_file.url
        else:
            return self.logo_url

    labour_event_meta = event_meta_property("labour")
    programme_event_meta = event_meta_property("programme")
    tickets_event_meta = event_meta_property("tickets")
    forms_event_meta = event_meta_property("forms")
    badges_event_meta = event_meta_property("badges")
    enrollment_event_meta = event_meta_property("enrollment")
    intra_event_meta = event_meta_property("intra")

    @property
    def program_v2_event_meta(self):
        """
        for program_v2, app_label is program_v2 but prefix is programv2
        so event_meta_property("programv2") did not
        """
        from program_v2.models import ProgramV2EventMeta

        try:
            return ProgramV2EventMeta.objects.get(event=self)
        except ProgramV2EventMeta.DoesNotExist:
            return None

    def get_app_event_meta(self, app_label: str):
        return getattr(self, f"{app_label}_event_meta")

    def as_dict(self, format="default"):
        if format == "default":
            return pick_attrs(
                self,
                "slug",
                "name",
                "homepage_url",
                "headline",
                organization=self.organization.as_dict(),
            )
        elif format == "listing":
            return pick_attrs(
                self,
                "slug",
                "name",
                "headline",
                "venue_name",
                "homepage_url",
                "start_time",
                "end_time",
                "cancelled",
            )
        else:
            raise NotImplementedError(format)

    def get_claims(self, **extra_claims):
        """
        Shorthand for commonly used CBAC claims.
        """
        return dict(organization=self.organization.slug, event=self.slug, **extra_claims)
