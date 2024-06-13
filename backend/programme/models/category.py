from django.db import models
from django.utils.translation import gettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify


class Category(models.Model):
    id: int

    event = models.ForeignKey("core.Event", on_delete=models.CASCADE)
    title = models.CharField(max_length=1023)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore
    style = models.CharField(max_length=15)
    notes = models.TextField(blank=True)
    public = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

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

    class Meta:
        ordering = ["event", "order", "title"]
        unique_together = [("event", "slug")]
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    @classmethod
    def get_or_create_dummy(cls):
        from .programme_event_meta import ProgrammeEventMeta

        meta, unused = ProgrammeEventMeta.get_or_create_dummy()

        return cls.objects.get_or_create(
            event=meta.event,
            title="Dummy category",
            defaults=dict(
                style="dummy",
            ),
        )

    @property
    def qualified_slug(self):
        return f"category-{self.slug}"

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
            self.v2_dimensions = {"category": [self.slug]}

        return super().save(*args, **kwargs)
