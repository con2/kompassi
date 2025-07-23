from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from kompassi.core.models.group_management_mixin import GroupManagementMixin


class AccessOrganizationMeta(models.Model, GroupManagementMixin):
    organization = models.OneToOneField(
        "core.Organization", on_delete=models.CASCADE, primary_key=True, verbose_name=_("organization")
    )
    admin_group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_("administrator group"))

    def __str__(self):
        return self.organization.name if self.organization is not None else "None"

    class Meta:
        verbose_name = _("access management settings")

    def get_group(self, suffix):
        group_name = self.make_group_name(self.organization, suffix)
        return Group.objects.get(name=group_name)
