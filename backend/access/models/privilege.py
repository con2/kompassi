from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core.utils.misc_utils import get_code
from core.utils.model_utils import make_slug_field

if TYPE_CHECKING:
    from .slack_access import SlackAccess


class Privilege(models.Model):
    slug = make_slug_field()
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    disclaimers = models.TextField(blank=True)
    request_success_message = models.TextField(blank=True)
    url = models.CharField(max_length=255, blank=True)

    grant_code = models.CharField(max_length=256)

    slack_access: models.ForeignKey[SlackAccess] | None
    id: int
    pk: int

    @classmethod
    def get_or_create_dummy(cls, slug="test-privilege"):
        GRANT_CODES = dict(
            test="access.privileges:add_to_group",
            slack="access.privileges:invite_to_slack",
        )

        return cls.objects.get_or_create(
            slug=slug,
            defaults=dict(
                title="Check this privilege",
                grant_code=GRANT_CODES[slug],
            ),
        )

    def grant(self, person):
        from .granted_privilege import GrantedPrivilege

        gp, created = GrantedPrivilege.objects.get_or_create(
            privilege=self, person=person, defaults=dict(state="approved")
        )

        if gp.state != "approved":
            return

        if "background_tasks" in settings.INSTALLED_APPS:
            from ..tasks import grant_privilege

            grant_privilege.delay(self.pk, person.pk)  # type: ignore
        else:
            self._grant(person)

    def _grant(self, person):
        from .granted_privilege import GrantedPrivilege

        gp = GrantedPrivilege.objects.get(privilege=self, person=person, state="approved")

        grant_function = get_code(self.grant_code)
        grant_function(self, person)

        gp.state = "granted"
        gp.save()

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

    class Meta:
        verbose_name = _("privilege")
        verbose_name_plural = _("privileges")
