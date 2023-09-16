from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from .dimension import ProgramDimensionValue


class Program(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE)
    title = models.CharField(max_length=1023)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField(blank=True, null=True)
    length = models.DurationField(blank=True, null=True)
    other_fields = models.JSONField(blank=True, default=dict)

    # denormalized fields
    cached_dimensions = models.JSONField()

    # related fields
    dimension_values: models.QuerySet["ProgramDimensionValue"]

    @property
    def end_time(self):
        if self.start_time and self.length:
            return self.start_time + self.length
        return None

    @property
    def _dimensions(self):
        """
        Used to populate cached_dimensions
        """
        # TODO should all event dimensions always be present, or only those with values?
        # TODO when dimensions are changed for an event, refresh all cached_dimensions
        dimensions = {dimension.slug: [] for dimension in self.event.dimensions.all()}
        for pdv in self.dimension_values.all():
            dimensions[pdv.dimension.slug].append(pdv.dimension_value.slug)
        return dimensions
