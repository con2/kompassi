from __future__ import annotations

from functools import cached_property
from itertools import groupby
from typing import TYPE_CHECKING

from django.db import models

from core.models.person import Person
from dimensions.models.universe import Universe

if TYPE_CHECKING:
    pass


class InvolvementToGroupMapping(models.Model):
    """
    Grant Involved people group membership for access to external systems.
    """

    universe = models.ForeignKey(Universe, on_delete=models.CASCADE, related_name="involvement_to_group_mappings")
    required_dimensions = models.JSONField(default=dict)
    group = models.ForeignKey("auth.Group", on_delete=models.CASCADE, related_name="+")

    class Meta:
        ordering = ("universe",)

    def __str__(self):
        return f"{self.formatted_required_dimensions} -> {self.group}"

    @property
    def formatted_required_dimensions(self) -> str:
        """
        >>> InvolvementToGroupMapping(required_dimensions={"dimension1": ["value1", "value2"], "dimension2": ["value3"]}).formatted_required_dimensions
        'dimension1=value1 dimension1=value2 dimension2=value3'
        """
        return " ".join(f"{dimension_slug}={value_slug}" for (dimension_slug, value_slug) in self.required_pairs)

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

    @classmethod
    def ensure(cls, universe: Universe, person: Person):
        user = person.user
        if user is None:
            return

        involvements = universe.active_involvements.filter(person=person)

        for group, itgms in groupby(cls.objects.filter(universe=universe).order_by("group"), key=lambda x: x.group):
            if any(
                itgm.required_pairs.issubset(involvement.dimensions_pairs)
                for itgm in itgms
                for involvement in involvements
            ):
                group.user_set.add(user)
            else:
                group.user_set.remove(user)
