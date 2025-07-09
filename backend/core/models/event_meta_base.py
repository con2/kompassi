from __future__ import annotations

from django.contrib.auth.models import Group
from django.db import models

from .event import Event
from .group_management_mixin import GroupManagementMixin


class EventMetaBase(models.Model, GroupManagementMixin):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, primary_key=True, related_name="%(class)s")
    admin_group = models.ForeignKey(Group, on_delete=models.CASCADE)

    use_cbac = False

    event_id: int
    admin_group_id: int

    class Meta:
        abstract = True

    def get_group(self, suffix):
        group_name = self.make_group_name(self.event, suffix)

        return Group.objects.get(name=group_name)

    def get_group_if_exists(self, suffix):
        group_name = self.make_group_name(self.event, suffix)

        return Group.objects.filter(name=group_name).first()

    def is_user_admin(self, user):
        """
        Bridge between legacy access control and CBAC. Users that can do anything in an event are considered
        admins of that event.
        """
        if self.use_cbac:
            from access.models.cbac_entry import CBACEntry

            return CBACEntry.is_allowed(user, self.event.get_claims(app=self._meta.app_label))
        else:
            return user.is_superuser or self.is_user_in_admin_group(user)
