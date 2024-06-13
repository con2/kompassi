from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify


class Tag(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    title = models.CharField(max_length=63)
    order = models.IntegerField(default=0)
    style = models.CharField(max_length=15, default="label-default")

    v2_dimensions = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            "dimension slug -> list of dimension value slugs. "
            "When program is imported to v2, dimension values indicated here are added to programs of this category."
        ),
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = slugify(self.title)

        if (
            self.slug
            and not self.v2_dimensions
            and self.event
            and (meta := self.event.program_v2_event_meta)
            and meta.importer_name == "default"
        ):
            self.v2_dimensions = {"tag": [self.slug]}

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")
        ordering = ["order"]
        unique_together = [
            ("event", "slug"),
        ]
