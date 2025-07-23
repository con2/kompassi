from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.core.models import Event
from kompassi.core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify


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
    def get_or_create_dummy(cls, event: Event | None = None):
        from .programme_event_meta import ProgrammeEventMeta

        if event is None:
            event, _ = Event.get_or_create_dummy()

        meta, unused = ProgrammeEventMeta.get_or_create_dummy(event=event)

        return cls.objects.get_or_create(
            event=event,
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

        return super().save(*args, **kwargs)
