from django.db import models
from django.utils.translation import gettext_lazy as _


class GroupPrivilege(models.Model):
    privilege = models.ForeignKey("access.Privilege", on_delete=models.CASCADE, related_name="group_privileges")
    group = models.ForeignKey("auth.Group", on_delete=models.CASCADE, related_name="group_privileges")
    event = models.ForeignKey(
        "core.Event", on_delete=models.CASCADE, null=True, blank=True, related_name="group_privileges"
    )

    def __str__(self):
        return f"{self.group.name if self.group else None} - {self.privilege.title if self.privilege else None}"

    class Meta:
        verbose_name = _("group privilege")
        verbose_name_plural = _("group privileges")

        unique_together = [("privilege", "group")]
