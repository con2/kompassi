from django.db import models

from core.utils import validate_slug
from localized_fields.models import LocalizedModel
from localized_fields.fields import LocalizedCharField


class Dimension(LocalizedModel):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="dimensions")
    slug = models.CharField(max_length=255, validators=[validate_slug])
    title = LocalizedCharField(max_length=1023)
    color = models.CharField(max_length=63, blank=True, default="")
    icon = models.FileField(upload_to="program_v2/dimension_icons", blank=True)

    class Meta:
        unique_together = ("event", "slug")


class DimensionValue(LocalizedModel):
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name="values")
    slug = models.CharField(max_length=255, validators=[validate_slug])
    title = LocalizedCharField(max_length=1023)
    override_color = models.CharField(max_length=63, blank=True, default="")
    override_icon = models.FileField(upload_to="program_v2/dimension_icons", blank=True)

    @property
    def color(self):
        return self.override_color or self.dimension.color

    @property
    def icon(self):
        return self.override_icon or self.dimension.icon

    class Meta:
        unique_together = ("dimension", "slug")


class ProgramDimensionValue(models.Model):
    program = models.ForeignKey(
        "program_v2.Program",
        on_delete=models.CASCADE,
        related_name="dimension_values",
    )
    dimension_value = models.ForeignKey(DimensionValue, on_delete=models.CASCADE)

    # TODO should PDV have a reference to the dimension, or should it be looked up via dimension_value?
    @property
    def dimension(self):
        return self.dimension_value.dimension

    class Meta:
        unique_together = ("program", "dimension_value")
