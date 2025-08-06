from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.core.models import EventMetaBase

from .count_badges_mixin import CountBadgesMixin


class BadgesEventMeta(EventMetaBase, CountBadgesMixin):
    real_name_must_be_visible = models.BooleanField(
        default=False,
        verbose_name=_("Require real name to be visible"),
        help_text=_(
            "In most events, it is up to the person carrying the badge to decide whether or not "
            "their real name is displayed in their badge. Some choose to go by their first name or nick "
            "name only. Some events have, however, decided to restrict this and require the first name and "
            "surname to be visible in all badges. If this option is selected, only the name display styles "
            '<em>Firstname Surname</em> and <em>Firstname "Nick" Surname</em> are effectively allowed.'
        ),
    )

    onboarding_access_group = models.ForeignKey(
        "auth.Group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Onboarding access group"),
        help_text=_("Members of this group are granted access to the onboarding view without being badges admins."),
        related_name="as_onboarding_access_group_for",
    )

    emperkelator_name = models.CharField(
        max_length=63,
        default="noop",
        verbose_name=_("Emperkelator"),
        choices=[
            ("noop", "Noop (no perks)"),
            ("simple", "Simple (perks from personnel class)"),
            ("tracon2024", "Tracon (2024)"),
            ("desucon2025", "Desucon (2025)"),
        ],
        help_text=_(
            "The emperkelator defines the perks of a volunteer in the event based on their involvement with the event."
        ),
    )

    @property
    def emperkelator(self):
        """
        Deprecated. Use Involvement instead.
        """
        from ..emperkelators.noop import NoopEmperkelator

        return NoopEmperkelator

    @classmethod
    def get_or_create_dummy(
        cls,
        emperkelator_name: str = "noop",
    ):
        from kompassi.core.models import Event

        event, unused = Event.get_or_create_dummy()
        (group,) = cls.get_or_create_groups(event, ["admins"])
        return cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=group,
                emperkelator_name=emperkelator_name,
            ),
        )

    # for CountBadgesMixin
    @property
    def badges(self):
        from .badge import Badge

        return Badge.objects.filter(personnel_class__event=self.event)

    def is_user_allowed_onboarding_access(self, user):
        if self.is_user_admin(user):
            return True

        return self.onboarding_access_group and self.is_user_in_group(user, self.onboarding_access_group)
