import logging
import typing

from django.contrib.postgres.fields import HStoreField
from django.db import models

from core.utils import log_delete, log_get_or_create, validate_slug

from ..consts import CATEGORY_DIMENSION_TITLE_LOCALIZED, ROOM_DIMENSION_TITLE_LOCALIZED, TAG_DIMENSION_TITLE_LOCALIZED

if typing.TYPE_CHECKING:
    from core.models import Event


logger = logging.getLogger("kompassi")


class Dimension(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE, related_name="dimensions")
    slug = models.CharField(max_length=255, validators=[validate_slug])
    title = HStoreField(blank=True, default=dict)
    color = models.CharField(max_length=63, blank=True, default="")
    icon = models.FileField(upload_to="program_v2/dimension_icons", blank=True)

    values: models.QuerySet["DimensionValue"]

    class Meta:
        unique_together = ("event", "slug")

    def __str__(self):
        return self.slug

    @classmethod
    def ensure_v1_default_dimensions(cls, event: "Event", clear=False):
        """
        For v1 import, this ensures that the default dimensions are present.
        Returns the default dimensions as a tuple.
        """
        from programme.models import Category, Room, Tag

        if clear:
            log_delete(logger, event.dimensions.all().delete())

        dimensions = []
        for ModelV1, slug, title_localized in (
            (Category, "category", CATEGORY_DIMENSION_TITLE_LOCALIZED),
            (Room, "room", ROOM_DIMENSION_TITLE_LOCALIZED),
            (Tag, "tag", TAG_DIMENSION_TITLE_LOCALIZED),
        ):
            dimension, created = Dimension.objects.get_or_create(
                event=event,
                slug=slug,
                defaults=dict(
                    title=title_localized,
                ),
            )

            log_get_or_create(logger, dimension, created)
            dimensions.append(dimension)

            for v1_instance in ModelV1.objects.filter(event=event):
                title = v1_instance.name if ModelV1 is Room else v1_instance.title  # type: ignore
                dv, created = DimensionValue.objects.get_or_create(
                    dimension=dimension,
                    slug=v1_instance.slug,
                    defaults=dict(
                        title=dict(fi=title),
                    ),
                )

                log_get_or_create(logger, dv, created)

        category_dimension, room_dimension, tag_dimension = dimensions
        return category_dimension, room_dimension, tag_dimension


class DimensionValue(models.Model):
    dimension = models.ForeignKey(Dimension, on_delete=models.CASCADE, related_name="values")
    slug = models.CharField(max_length=255, validators=[validate_slug])
    title = HStoreField(blank=True, default=dict)
    override_color = models.CharField(max_length=63, blank=True, default="")
    override_icon = models.FileField(upload_to="program_v2/dimension_icons", blank=True)

    def __str__(self):
        return self.slug

    @property
    def event(self) -> "Event":
        return self.dimension.event

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
        related_name="dimensions",
    )
    dimension = models.ForeignKey(
        Dimension,
        on_delete=models.CASCADE,
        related_name="+",
    )
    value = models.ForeignKey(
        DimensionValue,
        on_delete=models.CASCADE,
        related_name="+",
    )

    def __str__(self):
        return f"{self.dimension}={self.value}"

    @property
    def event(self) -> "Event":
        return self.dimension.event

    class Meta:
        unique_together = ("program", "value")
