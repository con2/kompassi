from django.utils.translation import gettext_lazy as _


class ProgrammeyThingamajieAdminHelperMixin:
    """
    Apply this mixin to anything that has .programme to get event and title columns in the admin list_display.
    """

    def admin_get_event(self):
        return self.programme.category.event if self.programme else None

    admin_get_event.short_description = _("Event")
    admin_get_event.admin_order_field = "programme__category__event"

    def admin_get_title(self):
        return self.programme.title if self.programme else None

    admin_get_title.short_description = _("Title")
    admin_get_title.admin_order_field = "programme__title"
