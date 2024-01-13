from django.utils.translation import gettext_lazy as _

from ...models import FreeformOrganizer
from ..helpers import ProgrammeyThingamajieAdminHelperMixin


class FreeformOrganizerAdminProxy(FreeformOrganizer, ProgrammeyThingamajieAdminHelperMixin):
    """
    Used by programme.admin. Provides some Django Admin only functionality for FreeformOrganizer.
    """

    class Meta:
        verbose_name = _("freeform organizer")
        verbose_name_plural = _("freeform organizers")
        proxy = True
