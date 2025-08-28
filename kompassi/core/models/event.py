from __future__ import annotations

import logging
import typing
from datetime import UTC, datetime, timedelta, tzinfo
from functools import cached_property
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from ..utils import SLUG_FIELD_PARAMS, event_meta_property, format_date, format_date_range, pick_attrs, slugify
from .organization import Organization
from .venue import Venue

if typing.TYPE_CHECKING:
    from kompassi.dimensions.models.scope import Scope
    from kompassi.dimensions.models.universe import Universe
    from kompassi.forms.models.survey import Survey
    from kompassi.involvement.models.involvement import Involvement
    from kompassi.involvement.models.meta import InvolvementEventMeta
    from kompassi.labour.models.personnel_class import PersonnelClass
    from kompassi.labour.models.signup import Signup
    from kompassi.program_v2.models import Program, ProgramV2EventMeta, ScheduleItem
    from kompassi.tickets_v2.models import TicketsV2EventMeta


logger = logging.getLogger(__name__)


def validate_timezone_name(value: str) -> None:
    try:
        ZoneInfo(value)
    except Exception as e:
        raise ValidationError(f"Invalid timezone name: {value}") from e


class Event(models.Model):
    id: int

    slug = models.CharField(**SLUG_FIELD_PARAMS)  # type: ignore

    name = models.CharField(max_length=63, verbose_name="Tapahtuman nimi")

    organization: models.ForeignKey[Organization] = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name="Järjestäjätaho",
        related_name="events",
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

    venue: models.ForeignKey[Venue] = models.ForeignKey(
        Venue,
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

    timezone_name = models.CharField(
        default="Europe/Helsinki",
        validators=[validate_timezone_name],
    )

    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    # related fields
    programs: models.QuerySet[Program]
    schedule_items: models.QuerySet[ScheduleItem]
    signup_set: models.QuerySet[Signup]
    surveys: models.QuerySet[Survey]
    personnel_classes: models.QuerySet[PersonnelClass]

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

    @cached_property
    def scope(self) -> Scope:
        from kompassi.dimensions.models import Scope

        return Scope.objects.get_or_create(
            event=self,
            defaults=dict(
                slug=self.slug,
                name=self.name,
                organization=self.organization,
            ),
        )[0]

    @property
    def panel_css_class(self):
        return self.organization.panel_css_class

    @property
    def name_and_year(self):
        return f"{self.name} ({self.start_time.year})" if self.start_time else self.name

    @property
    def formatted_start_and_end_date(self):
        # TODO honor locale (currently always uses Finnish format)
        if not self.start_time or not self.end_time:
            return ""
        return format_date_range(self.start_time, self.end_time)

    @property
    def formatted_end_date(self) -> str:
        return format_date(self.end_time)

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

    @cached_property
    def timezone(self) -> tzinfo:
        try:
            return ZoneInfo(self.timezone_name)
        except Exception:
            logger.warning(f"Invalid timezone name: {self.timezone_name}", exc_info=True)
            return UTC

    @cached_property
    def program_universe(self) -> Universe:
        """
        The Universe for Dimensions that are attached to program items.
        NOTE: Must return the same as ProgramV2EventMeta.universe.
        """
        from kompassi.program_v2.dimensions import get_program_universe

        return get_program_universe(self)

    @cached_property
    def involvement_universe(self) -> Universe:
        from kompassi.involvement.dimensions import get_involvement_universe

        return get_involvement_universe(self)

    @property
    def involvements(self) -> models.QuerySet[Involvement]:
        from kompassi.involvement.models.involvement import Involvement

        return Involvement.objects.filter(universe=self.involvement_universe)

    @classmethod
    def get_or_create_dummy(cls, name="Dummy event"):
        # TODO not the best place for this, encap. see also admin command core_update_maysendinfo
        from django.contrib.auth.models import Group

        from .organization import Organization
        from .venue import Venue

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
    def program_v2_event_meta(self) -> ProgramV2EventMeta | None:
        """
        for program_v2, app_label is program_v2 but prefix is programv2
        so event_meta_property("programv2") did not
        """
        from kompassi.program_v2.models import ProgramV2EventMeta

        # NOTE: Do not cache None
        meta: ProgramV2EventMeta | None = getattr(self, "_program_v2_event_meta", None)
        if meta is None:
            try:
                self._program_v2_event_meta = meta = ProgramV2EventMeta.objects.get(event=self)
            except ProgramV2EventMeta.DoesNotExist:
                meta = None

        return meta

    @property
    def tickets_v2_event_meta(self) -> TicketsV2EventMeta | None:
        from kompassi.tickets_v2.models import TicketsV2EventMeta

        # NOTE: Do not cache None
        meta = getattr(self, "_tickets_v2_event_meta", None)
        if meta is None:
            try:
                self._tickets_v2_event_meta = meta = TicketsV2EventMeta.objects.get(event=self)
            except TicketsV2EventMeta.DoesNotExist:
                meta = None

        return meta

    @property
    def involvement_event_meta(self) -> InvolvementEventMeta | None:
        from kompassi.involvement.models.meta import InvolvementEventMeta

        # NOTE: Do not cache None
        meta = getattr(self, "_involvement_event_meta", None)
        if meta is None:
            try:
                self._involvement_event_meta = meta = InvolvementEventMeta.objects.get(event=self)
            except InvolvementEventMeta.DoesNotExist:
                meta = None

        return meta

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

    @classmethod
    def get_or_create_lite_event(
        cls,
        slug: str,
        name: str,
        organization_name: str,
        venue_name: str,
        start_time: datetime,
        end_time: datetime,
        public: bool = True,
        homepage_url: str = "",
    ):
        """
        Create an event for pure V2 use with minimal information required.
        Can be used out of the box with Surveys V2.
        """
        # if created here, these need to be fixed via taka-admin at least for the inflected names
        organization, _ = Organization.objects.get_or_create(
            slug=slugify(organization_name),
            defaults=dict(
                name=organization_name,
                name_genitive=organization_name,
            ),
        )
        venue, _ = Venue.objects.get_or_create(
            name=venue_name,
            defaults=dict(
                name_inessive=venue_name,
            ),
        )

        return cls.objects.get_or_create(
            slug=slug,
            defaults=dict(
                name=name,
                name_genitive=f"{name} -tapahtuman",
                name_illative=f"{name} -tapahtumaan",
                name_inessive=f"{name} -tapahtumassa",
                organization=organization,
                venue=venue,
                start_time=start_time,
                end_time=end_time,
                public=public,
                homepage_url=homepage_url,
            ),
        )
