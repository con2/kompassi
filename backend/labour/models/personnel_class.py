import logging

from django.db import models
from django.utils.translation import gettext_lazy as _
from markdown import markdown

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify

logger = logging.getLogger("kompassi")


class PersonnelClass(models.Model):
    event = models.ForeignKey("core.Event", on_delete=models.CASCADE)
    app_label = models.CharField(max_length=63, blank=True, default="labour")
    name = models.CharField(max_length=63)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)
    priority = models.IntegerField(default=0)
    icon_css_class = models.CharField(max_length=63, default="fa-user", blank=True)
    perks_markdown = models.TextField(
        verbose_name=_("perks"),
        blank=True,
        default="",
        help_text=_("Focus on things that are given to the person at check-in. Markdown formatting available."),
    )

    class Meta:
        verbose_name = _("personnel class")
        verbose_name_plural = _("personnel classes")

        unique_together = [
            ("event", "slug"),
        ]

        index_together = [
            ("event", "app_label"),
        ]

        ordering = ("event", "priority")

    @classmethod
    def get_or_create_dummy(cls, app_label="labour", name="Smallfolk", priority=0):
        from core.models import Event

        event, unused = Event.get_or_create_dummy()

        return PersonnelClass.objects.get_or_create(
            event=event,
            slug=slugify(name),
            app_label=app_label,
            defaults=dict(
                name=app_label,
                priority=priority,
            ),
        )

    @property
    def perks_html(self):
        """
        See also badges_admin_onboarding_view.(py|pug).
        """
        return markdown(self.perks_markdown) if self.perks_markdown else ""

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
