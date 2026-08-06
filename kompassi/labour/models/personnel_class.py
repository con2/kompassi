from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.core.models import Event
from kompassi.core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify
from kompassi.core.utils.log_utils import log_delete

if TYPE_CHECKING:
    from kompassi.badges.models.badge import Badge

    from .signup import Signup

logger = logging.getLogger(__name__)


class PersonnelClass(models.Model):
    event: models.ForeignKey[Event] = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="personnel_classes",
    )
    app_label = models.CharField(max_length=63, blank=True, default="labour")
    name = models.CharField(max_length=63)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore
    priority = models.IntegerField(default=0)
    icon_css_class = models.CharField(max_length=63, default="fa-user", blank=True)
    perks = models.JSONField(default=dict, blank=True)
    override_formatted_perks = models.TextField(default="", blank=True)

    signups: models.QuerySet[Signup]
    badges: models.QuerySet[Badge]

    class Meta:
        verbose_name = _("personnel class")
        verbose_name_plural = _("personnel classes")
        unique_together = [("event", "slug")]  # noqa: RUF012
        indexes = [models.Index(fields=["event", "app_label"])]  # noqa: RUF012
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
        from kompassi.core.models import Event

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

    def delete_unused(self):
        """
        Deletes this Personnel Class only if it is unused.
        Raises a ValueError if there are any Signups or Badges in it.
        """
        if self.signups.exists():
            raise ValueError(f"Refusing to PersonnelClass.delete_unused {self} ({self.event}): signups present")

        if self.badges.exists():
            raise ValueError(f"Refusing to PersonnelClass.delete_unused {self} ({self.event}): badges present")

        delete_result = self.delete()

        log_delete(
            logger,
            delete_result,
            zero_level=None,
            message="Unused personnel class removed",
            event=self.event.slug,
            personnel_class=self.slug,
        )

        return delete_result

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
