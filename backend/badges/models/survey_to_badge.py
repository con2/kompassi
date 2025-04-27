from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from labour.models.personnel_class import PersonnelClass


class SurveyToBadgeMapping(models.Model):
    """
    Create badges for people who have filled out a survey and match the required dimensions.
    Part of Survey to Badge (STB). See https://outline.con2.fi/doc/survey-to-badge-stb-mxK1UW6hAn
    """

    survey = models.ForeignKey("forms.Survey", on_delete=models.CASCADE, related_name="badge_mappings")
    required_dimensions = models.JSONField(default=dict)
    personnel_class = models.ForeignKey(
        "labour.PersonnelClass",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="badge_mappings",
    )
    job_title = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return f"{self.survey} -> {self.personnel_class}"

    @cached_property
    def required_pairs(self) -> set[tuple[str, str]]:
        """
        Returns a set of tuples (dimension_slug, value_slug) for the required dimensions.
        """
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

    def match(self, person) -> list[tuple[PersonnelClass, str]]:
        if person.user is None:
            return []

        matches = []

        for response in self.survey.responses.filter(created_by=person.user):
            present_pairs = {
                (dimension_slug, value_slug)
                for dimension_slug, value_slugs in response.cached_dimensions.items()
                for value_slug in value_slugs
            }

            if self.required_pairs.issubset(present_pairs):
                matches.append((self.personnel_class, self.some_job_title))

        return matches
