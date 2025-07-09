import logging
from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Event
from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify

logger = logging.getLogger("kompassi")


class PersonnelClass(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE)
    app_label = models.CharField(max_length=63, blank=True, default="labour")
    name = models.CharField(max_length=63)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore
    priority = models.IntegerField(default=0)
    icon_css_class = models.CharField(max_length=63, default="fa-user", blank=True)
    perks = models.JSONField(default=dict, blank=True)
    override_formatted_perks = models.TextField(default="", blank=True)

    class Meta:
        verbose_name = _("personnel class")
        verbose_name_plural = _("personnel classes")
        unique_together = [("event", "slug")]
        indexes = [models.Index(fields=["event", "app_label"])]
        ordering = ("event", "priority")

    @classmethod
    def get_or_create_dummy(
        cls,
        app_label="labour",
        name="Smallfolk",
        priority=0,
        event: Event | None = None,
        perks: dict[str, Any] | None = None,
    ):
        from core.models import Event

        if event is None:
            event, _ = Event.get_or_create_dummy()

        return PersonnelClass.objects.get_or_create(
            event=event,
            slug=slugify(name),
            app_label=app_label,
            defaults=dict(
                name=app_label,
                priority=priority,
                perks=perks or {},
            ),
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
