from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...models import FreeformOrganizer
from ..helpers import ProgrammeyThingamajieAdminHelperMixin


class FreeformOrganizerAdminProxy(FreeformOrganizer, ProgrammeyThingamajieAdminHelperMixin):
    """
    Used by programme.admin. Provides some Django Admin only functionality for FreeformOrganizer.
    """

    class Meta:
        verbose_name = _(u'freeform organizer')
        verbose_name_plural = _(u'freeform organizers')
        proxy = True