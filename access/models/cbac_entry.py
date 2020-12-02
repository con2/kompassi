from datetime import datetime
from typing import Dict

from django.conf import settings
from django.contrib.postgres.fields import HStoreField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

from core.utils import get_objects_within_period


Claims = Dict[str, str]


class CBACEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cbac_entries')

    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()

    mode = models.CharField(
        max_length=1,
        choices=[('+', 'Allow'), ('-', 'Deny'), ('0', 'Inactive')],
        default='+',
    )

    claims = HStoreField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    granted_by_group = models.ForeignKey('auth.Group', on_delete=models.CASCADE, null=True, blank=True, related_name='+')

    def __str__(self):
        if not self.claims:
            return f"user={self.user.username} – EMPTY CLAIMS, ALLOWED TO DO ANYTHING"
        else:
            return ", ".join(f"{key}={value}" for (key, value) in dict(user=self.user.username, **self.claims).items())

    class Meta:
        index_together = [('user', 'mode', 'valid_until')]

    def save(self, *args, **kwargs):
        if not self.valid_from:
            self.valid_from = now()

        return super().save(*args, **kwargs)

    @classmethod
    def get_entries(cls, user: AbstractUser, claims: Claims = None, t: datetime = None, **kwargs):
        queryset = get_objects_within_period(
            cls,
            t=t,
            start_field_name='valid_from',
            end_field_name='valid_until',
            end_field_nullable=False,
            user=user,
        )

        if claims is not None:
            queryset = queryset.filter(claims__contained_by=claims)

        return queryset

    @classmethod
    def is_allowed(cls, user: AbstractUser, claims: Claims, t: datetime = None):
        entries = cls.get_entries(user, claims, t=t)
        return entries.filter(mode='+').exists() and not entries.filter(mode='-').exists()
