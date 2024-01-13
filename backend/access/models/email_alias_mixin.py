from django.utils.translation import gettext_lazy as _


class EmailAliasMixin:
    def admin_get_organization(self):
        return self.domain.organization if self.domain else None

    admin_get_organization.short_description = _("organization")
    admin_get_organization.admin_order_field = "type__domain__organization"

    def _make_email_address(self):
        return f"{self.account_name}@{self.domain.domain_name}" if self.account_name and self.domain else None
