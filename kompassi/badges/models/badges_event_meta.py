from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from kompassi.core.models import EventMetaBase
from kompassi.core.utils.retention_period import retention_reference_time

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

    # NOTE: lazy reference is mandatory: involvement.models.involvement imports badges at module level.
    registry = models.ForeignKey(
        "involvement.Registry",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Registry"),
        help_text=_(
            "The personal data registry the badges of this event belong to. Badges are deleted after the "
            "default retention period of the registry has passed since the end of the year in which the event ends."
        ),
        related_name="badges_event_metas",
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

    @property
    def badge_retention_expired(self) -> bool:
        """
        Whether the retention period for the badges of this event has expired.

        NOTE: The anchor is the end time of the event only, with no fallback to the creation time
        of the badge. Badge.ensure consults this to avoid recreating a swept badge, and it cannot
        see a per-badge creation time; a fallback here would make an end-time-less event's badge
        oscillate between swept and resurrected. Must stay in sync with
        Badge.get_expired_badges_for_cleanup.
        """
        if self.registry is None or self.registry.default_retention_period is None:
            return False
        if self.event.end_time is None:
            return False

        return retention_reference_time(self.event.end_time) + self.registry.default_retention_period < now()

    @classmethod
    def get_or_create_dummy(cls):
        from kompassi.core.models import Event

        event, _unused = Event.get_or_create_dummy()
        (group,) = cls.get_or_create_groups(event, ["admins"])
        return cls.objects.get_or_create(
            event=event,
            defaults=dict(
                admin_group=group,
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
