from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from django.db import models

from kompassi.dimensions.models.universe import Universe

from .involvement import Involvement

if TYPE_CHECKING:
    from kompassi.labour.models.personnel_class import PersonnelClass


class InvolvementToBadgeMapping(models.Model):
    """
    Create badges for Involved people who match the required dimensions.
    """

    universe: models.ForeignKey[Universe] = models.ForeignKey(
        Universe,
        on_delete=models.CASCADE,
        related_name="involvement_to_badge_mappings",
    )
    required_dimensions = models.JSONField(default=dict)
    personnel_class = models.ForeignKey(
        "labour.PersonnelClass",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="involvement_to_badge_mappings",
    )
    job_title = models.CharField(max_length=255, blank=True, default="")
    priority = models.IntegerField(default=0, help_text="smallest number is the highest priority")
    annotations = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ("universe", "priority")

    def __str__(self):
        return f"{self.universe} -> {self.personnel_class}"

    @property
    def formatted_required_dimensions(self) -> str:
        return " ".join(f"{dimension_slug}={value_slug}" for (dimension_slug, value_slug) in self.required_pairs)

    @cached_property
    def required_pairs(self) -> set[tuple[str, str]]:
        return {
            (dimension_slug, value_slug)
            for dimension_slug, value_slugs in self.required_dimensions.items()
            for value_slug in value_slugs
        }

    @property
    def some_job_title(self) -> str:
        if self.job_title:
            return self.job_title
        return self.personnel_class.name

    def match(self, person) -> list[tuple[Involvement, PersonnelClass, str]]:
        if person.user is None:
            return []

        matches: list[tuple[Involvement, PersonnelClass, str]] = []

        for involvement in self.universe.active_involvements.filter(person=person):
            present_pairs = {
                (dimension_slug, value_slug)
                for dimension_slug, value_slugs in involvement.cached_dimensions.items()
                for value_slug in value_slugs
            }

            if self.required_pairs.issubset(present_pairs):
                matches.append((involvement, self.personnel_class, self.some_job_title))

        return matches
