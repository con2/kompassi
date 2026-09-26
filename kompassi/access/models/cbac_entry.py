from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Self

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, Group
from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils.timezone import now

from kompassi.core.utils import get_objects_within_period, log_get_or_create
from kompassi.core.utils.cleanup import register_cleanup
from kompassi.event_log_v2.utils.emit import emit
from kompassi.intra.constants import SUPPORTED_APPS

from ..constants import CBAC_VALID_AFTER_EVENT_DAYS

Claims = dict[str, str]
logger = logging.getLogger(__name__)


class CBACEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cbac_entries")

    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()

    claims = HStoreField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    granted_by_group = models.ForeignKey(
        "auth.Group", on_delete=models.CASCADE, null=True, blank=True, related_name="+"
    )

    def __str__(self):
        return ", ".join(f"{key}={value}" for (key, value) in dict(user=self.user.username, **self.claims).items())

    class Meta:
        indexes = [models.Index(fields=["user", "valid_until"])]  # noqa: RUF012

    def save(self, *args, **kwargs):
        if not self.valid_from:
            self.valid_from = now()

        return super().save(*args, **kwargs)

    def as_dict(self) -> dict[str, Any]:
        return dict(
            user=self.user.username,
            valid_from=self.valid_from.isoformat(),
            valid_until=self.valid_until.isoformat(),
            claims=self.claims,
            granted_by_group=self.granted_by_group.name if self.granted_by_group else "",
        )

    @classmethod
    def get_entries(
        cls,
        user: AbstractBaseUser | AnonymousUser,
        claims: Claims | None = None,
        t: datetime | None = None,
        **extra_criteria,
    ):
        if not user.is_authenticated:
            return cls.objects.none()

        queryset = get_objects_within_period(
            cls,
            t=t,
            start_field_name="valid_from",
            end_field_name="valid_until",
            end_field_nullable=False,
            user=user,
            **extra_criteria,
        )

        if claims is not None:
            queryset = queryset.filter(claims__contained_by=claims)

        return queryset

    @classmethod
    def is_allowed(
        cls,
        user: AbstractBaseUser | AnonymousUser,
        claims: Claims,
        t: datetime | None = None,
    ) -> bool:
        if not user.is_authenticated:
            return False

        return cls.get_entries(
            user,  # type: ignore
            claims,
            t=t,
        ).exists()

    @classmethod
    def grant_access(
        cls,
        user: AbstractBaseUser,
        claims: Claims,
        expires_at: datetime,
        *,
        valid_from: datetime | None = None,
        created_by: AbstractBaseUser | None = None,
        granted_by_group: Group | None = None,
    ) -> tuple[Self | None, bool]:
        """
        Grant `user` access matching `claims` until `expires_at`. No-ops (logging a
        warning instead of granting anything) if `expires_at` has already passed, so
        callers can compute an event-relative expiry without checking it against
        `now()` themselves.
        """
        if expires_at < now():
            logger.warning(
                "CBAC: not granting %r access to claims=%r because expires_at=%s is already in the past",
                user,
                claims,
                expires_at,
            )
            return None, False

        # (user, claims) is not unique in the database, so a production dump can hold
        # duplicates. Any one of them grants the access, so the newest is reused.
        existing = cls.objects.filter(user=user, claims=claims).order_by("-valid_until", "-id")
        entries = list(existing[:2])
        if len(entries) > 1:
            logger.warning(
                "CBAC: duplicate entries for user and claims, reusing the newest",
                extra=dict(user=user.pk, claims=claims, entry=entries[0].pk),
            )
        if entries:
            return entries[0], False

        entry = cls.objects.create(
            user=user,
            claims=claims,
            valid_from=valid_from or now(),
            valid_until=expires_at,
            created_by=created_by,
            granted_by_group=granted_by_group,
        )
        log_get_or_create(logger, entry, True)

        return entry, True

    @classmethod
    def ensure_admin_group_privileges(cls, t: datetime | None = None):
        from kompassi.core.models import Event

        if t is None:
            t = now()

        for event in Event.objects.filter(end_time__gte=t):
            cls.ensure_admin_group_privileges_for_event(event, t=t)

    @classmethod
    def ensure_admin_group_privileges_for_event(
        cls,
        event,
        *,
        t: datetime | None = None,
        request=None,
    ):
        if t is None:
            t = now()

        for app_name in SUPPORTED_APPS:
            meta = event.get_app_event_meta(app_name)

            if not meta:
                continue

            admin_group = meta.admin_group
            admin_group_members = admin_group.user_set.all()

            # remove access from those who should not have it
            entries_to_remove = cls.objects.filter(granted_by_group=admin_group).exclude(user__in=admin_group_members)
            for cbac_entry in entries_to_remove:
                emit(
                    "access.cbacentry.deleted",
                    request=request,
                    other_fields=cbac_entry.as_dict(),
                )
            entries_to_remove.delete()

            # add access to those who should have it but do not yet have
            for user in admin_group_members:
                cbac_entry, created = cls.grant_access(
                    user,
                    claims={
                        "organization": event.organization.slug,
                        # omit "event" to give permissions also to other events of same organizer
                        # "event": event.slug,
                        "app": app_name,
                    },
                    expires_at=event.end_time + timedelta(CBAC_VALID_AFTER_EVENT_DAYS),
                    valid_from=t,
                    created_by=request.user if request else None,
                    granted_by_group=admin_group,
                )
                if created and cbac_entry is not None:
                    emit(
                        "access.cbacentry.created",
                        request=request,
                        other_fields=cbac_entry.as_dict(),
                    )

    @classmethod
    def get_entries_for_cleanup(cls, queryset: models.QuerySet[Self]):
        """
        Cleanup filter used by @register_cleanup.
        As a side effect, emits an event for each expired entry.
        """
        expired_entries = cls.objects.filter(valid_until__lt=now())

        for cbac_entry in expired_entries:
            emit(
                "access.cbacentry.expired",
                other_fields=cbac_entry.as_dict(),
            )

        return expired_entries


register_cleanup(CBACEntry.get_entries_for_cleanup)(CBACEntry)
