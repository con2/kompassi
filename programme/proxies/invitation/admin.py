from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...models import Invitation
from ..helpers import ProgrammeyThingamajieAdminHelperMixin


class InvitationAdminProxy(Invitation, ProgrammeyThingamajieAdminHelperMixin):
    """
    Used by programme.admin. Provides some Django Admin only functionality for Invitation.
    """

    class Meta:
        verbose_name = _(u'invitation')
        verbose_name_plural = _(u'invitations')
        proxy = True