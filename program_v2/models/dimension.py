from django.db import models

from core.utils import validate_slug


class Dimension(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="dimensions")
    slug = models.CharField(max_length=255, validators=[validate_slug])
    title = models.CharField(max_length=1023)

    class Meta:
        unique_together = ("event", "slug")


class DimensionValue(models.Model):
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name="values")
    slug = models.CharField(max_length=255, validators=[validate_slug])
    title = models.CharField(max_length=1023)

    class Meta:
        unique_together = ("dimension", "slug")


class ProgramDimensionValue(models.Model):
    program = models.ForeignKey(
        "program_v2.Program",
        on_delete=models.CASCADE,
        related_name="dimension_values",
    )
    dimension_value = models.ForeignKey(DimensionValue, on_delete=models.CASCADE)

    @property
    def dimension(self):
        return self.dimension_value.dimension

    class Meta:
        unique_together = ("program", "dimension_value")
