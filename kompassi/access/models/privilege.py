from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse

from kompassi.core.utils.model_utils import make_slug_field

if TYPE_CHECKING:
    from .slack_access import SlackAccess


class PrivilegeType(Enum):
    SLACK = "SLACK"


class Privilege(models.Model):
    slug = make_slug_field()
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    disclaimers = models.TextField(blank=True)
    request_success_message = models.TextField(blank=True)
    url = models.CharField(max_length=255, blank=True)

    type_slug = models.CharField(
        max_length=max(len(pt.value) for pt in PrivilegeType),
        choices=[(pt.value, pt.value) for pt in PrivilegeType],
        default=PrivilegeType.SLACK.value,
        verbose_name="type",
    )

    slack_access: models.ForeignKey[SlackAccess] | None
    id: int
    pk: int

    @property
    def type(self) -> PrivilegeType:
        return PrivilegeType(self.type_slug)

    @classmethod
    def get_or_create_dummy(cls, slug="test-privilege"):
        return cls.objects.get_or_create(
            slug=slug,
            defaults=dict(
                title="Check this privilege",
            ),
        )

    def grant(self, person):
        from .granted_privilege import GrantedPrivilege

        GrantedPrivilege.objects.get_or_create(
            privilege=self,
            person=person,
            defaults=dict(state="approved"),
        )

        # Slack invite is handled by invite link client-side and requires no server-side interaction.
        # If further privilege types are added, implement them here.
        match self.type:
            case PrivilegeType.SLACK:
                pass
            case other:
                raise NotImplementedError(other)

    @classmethod
    def get_potential_privileges(cls, person, **extra_criteria):
        if not person.user:
            raise ValueError("person.user must be set")
        return (
            cls.objects.filter(group_privileges__group__in=person.user.groups.all(), **extra_criteria)
            .exclude(granted_privileges__person=person)
            .distinct()
        )

    def get_absolute_url(self):
        return f"{reverse('access_profile_privileges_view')}#privilege-{self.id}"

    def __str__(self):
        return self.title
