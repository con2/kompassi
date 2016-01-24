from django.db import models
from django.utils.translation import ugettext_lazy as _

from ...models import Invitation


class InvitationAdminProxy(Invitation):
    """
    Used by programme.admin. Provides some Django Admin only functionality for Invitation.
    """

    def admin_get_event(self):
        return self.programme.category.event if self.programme else None
    admin_get_event.short_description = _(u'Event')
    admin_get_event.admin_order_field = 'programme__category__event'

    def admin_get_title(self):
        return self.programme.title if self.programme else None
    admin_get_title.short_description = _(u'Title')
    admin_get_title.admin_order_field = 'programme__title'

    class Meta:
        verbose_name = _(u'invitation')
        verbose_name_plural = _(u'invitations')
        proxy = True