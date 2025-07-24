from __future__ import annotations

import logging
from functools import cached_property
from typing import TYPE_CHECKING

from django.db import models
from django.db.models import Q

from ..utils import SLUG_FIELD_PARAMS, pick_attrs, slugify

if TYPE_CHECKING:
    from kompassi.access.models import AccessOrganizationMeta
    from kompassi.membership.models import MembershipOrganizationMeta
    from kompassi.payments.models import PaymentsOrganizationMeta

    from .event import Event


logger = logging.getLogger(__name__)


class Organization(models.Model):
    slug = models.CharField(**SLUG_FIELD_PARAMS)  # type: ignore

    name = models.CharField(max_length=255, verbose_name="Nimi")
    name_genitive = models.CharField(max_length=255, verbose_name="Nimi genetiivissä")

    description = models.TextField(blank=True, verbose_name="Kuvaus")
    homepage_url = models.CharField(blank=True, max_length=255, verbose_name="Kotisivu")
    muncipality = models.CharField(
        blank=True,
        max_length=127,
        verbose_name="Yhdistyksen kotipaikka",
        help_text="Kunta, johon yhdistys on rekisteröity.",
    )
    public = models.BooleanField(
        default=False,
        verbose_name="Julkinen",
        help_text="Julkisilla yhdistyksillä on yhdistyssivu ja ne näytetään etusivulla.",
    )

    logo_url = models.CharField(
        blank=True,
        max_length=255,
        default="",
        verbose_name="Organisaation logon URL",
        help_text="Voi olla paikallinen (alkaa /-merkillä) tai absoluuttinen (alkaa http/https)",
    )

    panel_css_class = models.CharField(
        blank=True,
        max_length=255,
        default="panel-default",
        verbose_name="Etusivun paneelin väri",
        choices=[
            ("panel-default", "Harmaa"),
            ("panel-primary", "Kompassi (turkoosi)"),
            ("panel-success", "Desucon (vihreä)"),
            ("panel-info", "Yukicon (vaaleansininen)"),
            ("panel-warning", "Popcult (oranssi)"),
            ("panel-danger", "Tracon (punainen)"),
            ("panel-ropecon panel-default", "Ropecon (violetti)"),
        ],
    )

    events: models.QuerySet[Event]
    membershiporganizationmeta: models.OneToOneField[MembershipOrganizationMeta]
    accessorganizationmeta: models.OneToOneField[AccessOrganizationMeta]
    paymentsorganizationmeta: models.OneToOneField[PaymentsOrganizationMeta]

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        if self.name and not self.name_genitive:
            if self.name.endswith(" ry"):
                self.name_genitive = self.name + ":n"
            else:
                self.name_genitive = self.name + "n"

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @cached_property
    def scope(self):
        from kompassi.dimensions.models import Scope

        return Scope.objects.get_or_create(
            organization=self,
            event=None,
            defaults=dict(
                slug=self.slug,
                name=self.name,
            ),
        )[0]

    @classmethod
    def get_or_create_dummy(cls):
        return cls.objects.get_or_create(
            slug="dummy-organization",
            defaults=dict(
                name="Dummy organization",
                homepage_url="http://example.com",
            ),
        )

    @property
    def membership_organization_meta(self):
        from kompassi.membership.models import MembershipOrganizationMeta

        try:
            return self.membershiporganizationmeta
        except MembershipOrganizationMeta.DoesNotExist:
            return None

    @property
    def access_organization_meta(self):
        from kompassi.access.models import AccessOrganizationMeta

        try:
            return self.accessorganizationmeta
        except AccessOrganizationMeta.DoesNotExist:
            return None

    @property
    def payments_organization_meta(self):
        from kompassi.payments.models import PaymentsOrganizationMeta

        try:
            return self.paymentsorganizationmeta
        except PaymentsOrganizationMeta.DoesNotExist:
            return None

    @property
    def people(self):
        """
        Returns people with involvement in events of the current organization
        """
        from .person import Person

        # have signups
        q = Q(signups__event__organization=self)

        # have archived signups
        q |= Q(archived_signups__event__organization=self)

        # or programmes
        q |= Q(programme_roles__programme__category__event__organization=self)

        # or are members
        q |= Q(memberships__organization=self)

        # or have enrolled
        q |= Q(enrollment__event__organization=self)

        return Person.objects.filter(q).distinct()

    def as_dict(self):
        return pick_attrs(
            self,
            "slug",
            "name",
            "homepage_url",
        )

    class Meta:
        verbose_name = "Organisaatio"
        verbose_name_plural = "Organisaatiot"
