from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify

if TYPE_CHECKING:
    from .programme import Programme


class Tag(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    title = models.CharField(max_length=63)
    order = models.IntegerField(default=0)
    style = models.CharField(max_length=15, default="label-default")

    public = models.BooleanField(default=True)

    v2_dimensions = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            "dimension slug -> list of dimension value slugs. "
            "When program is imported to v2, dimension values indicated here are added to programs of this category."
        ),
    )

    programme_set: models.QuerySet[Programme]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")
        ordering = ["order"]
        unique_together = [
            ("event", "slug"),
        ]
