from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Event
from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS


class Role(models.Model):
    personnel_class = models.ForeignKey(
        "labour.PersonnelClass",
        on_delete=models.CASCADE,
        verbose_name=_("Personnel class"),
        help_text=_("The personnel class for the programme hosts that have this role."),
    )

    title = models.CharField(
        max_length=1023,
        verbose_name=_("Job title"),
    )

    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)  # type: ignore

    override_public_title = models.CharField(
        max_length=63,
        blank=True,
        verbose_name=_("Override public job title"),
        help_text=_("This gets displayed publicly instead of title, if set. Affects eg. badges."),
    )

    require_contact_info = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    is_public = models.BooleanField(
        default=True,
        verbose_name=_("Public"),
        help_text=_("Only hosts who are assigned public roles will be shown publicly in the programme schedule."),
    )

    priority = models.IntegerField(
        default=0,
        verbose_name=_("Priority"),
        help_text=_(
            "Some events have speaker roles that convey different privileges within the same personnel class. This priority field will put the speakers in their place."
        ),
    )

    perks = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Perks"),
        help_text=_("Perks for this role"),
    )

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")
        ordering = ("personnel_class__event", "personnel_class__priority", "priority")

    def __str__(self):
        return self.title

    @property
    def public_title(self):
        """
        This is what gets printed in the badge as the job title.
        Uses override_public_title to override title if present.
        """
        return self.override_public_title if self.override_public_title else self.title

    @classmethod
    def get_or_create_dummy(
        cls,
        personnel_class=None,
        priority=0,
        title="Overbaron",
        perks: dict[str, int | bool] | None = None,
        event: Event | None = None,
    ):
        from labour.models import PersonnelClass

        if event is None:
            event, _ = Event.get_or_create_dummy()

        if personnel_class is None:
            personnel_class, _ = PersonnelClass.get_or_create_dummy(
                app_label="programme",
                name="Entertainer",
                priority=40,
                event=event,
            )

        return cls.objects.get_or_create(
            personnel_class=personnel_class,
            title=title,
            defaults=dict(
                priority=priority,
                require_contact_info=False,
                perks=perks or dict(),
            ),
        )

    def admin_get_event(self):
        return self.personnel_class.event if self.personnel_class else None

    admin_get_event.short_description = _("Event")
    admin_get_event.admin_order_field = "personnel_class__event"
