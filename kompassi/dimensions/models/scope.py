from __future__ import annotations

from functools import cache, cached_property
from typing import TYPE_CHECKING

from django.db import models

from kompassi.core.models.event import Event
from kompassi.core.models.organization import Organization
from kompassi.core.utils.model_utils import make_slug_field, slugify

if TYPE_CHECKING:
    from kompassi.involvement.models.registry import Registry

    from .universe import Universe


class Scope(models.Model):
    """
    Scope is the first level of categorization in SURR (Scope and Use Case Routing and redirection).

    The scope in the first phase shall be either

    1. an Event,
    2. an Organization, or
    3. the "special" scope Kompassi.

    For more information, see SURR in Con2 Outline:
    https://outline.con2.fi/doc/scope-and-use-case-routing-and-redirection-surr-PwKuvWqLYC
    https://outline.con2.fi/s/d118043a-2dc9-430c-90e1-0e4ca6255191
    """

    # core.Event.name.max_length=63, core.Organization.name.max_length=255
    name = models.CharField(max_length=255)
    slug = make_slug_field(unique=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    event: models.ForeignKey[Event] | None = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    registries: models.QuerySet[Registry]
    universes: models.QuerySet[Universe]

    def __str__(self):
        return self.slug

    @classmethod
    @cache
    def get_root_scope(cls):
        return cls.objects.get_or_create(
            slug="kompassi",
            defaults=dict(
                name="Kompassi",
            ),
        )[0]

    def save(self, *args, **kwargs):
        if self.organization is None and self.event is not None:
            self.organization = self.event.organization

        if not self.name:
            match self.organization, self.event:
                case (None, None):
                    self.name = "Kompassi"
                case (organization, None):
                    self.name = organization.name
                case (_, event):
                    self.name = event.name

        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    @cached_property
    def cbac_claims(self):
        claims = dict(scope=self.slug)

        if self.organization:
            if self.event:
                claims.update(event=self.event.slug, organization=self.organization.slug)
            else:
                claims.update(organization=self.organization.slug)

        return claims

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "event"],
                nulls_distinct=False,
                name="scope_unique_organization_event",
            ),
            models.CheckConstraint(
                condition=~models.Q(organization=None, event__isnull=False),
                name="scope_disallow_event_without_organization",
            ),
        ]
