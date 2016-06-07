# encoding: utf-8

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


class EmailAliasMixin(object):
    def admin_get_organization(self):
        return self.domain.organization if self.domain else None
    admin_get_organization.short_description = _('organization')
    admin_get_organization.admin_order_field = 'type__domain__organization'

    def _make_email_address(self):
        return '{account_name}@{domain}'.format(
            account_name=self.account_name,
            domain=self.domain.domain_name,
        ) if self.account_name and self.domain else None
