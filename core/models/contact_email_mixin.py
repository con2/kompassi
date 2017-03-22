# encoding: utf-8



import re
import logging

from django.core.validators import RegexValidator


logger = logging.getLogger('kompassi')

CONTACT_EMAIL_RE = re.compile(r'(?P<name>.+) <(?P<email>.+@.+\..+)>')
contact_email_validator = RegexValidator(CONTACT_EMAIL_RE)


class ContactEmailMixin(object):
    def match_contact_email(self):
        if not self.contact_email:
            logger.warn('%s for %s has no contact_email', self.__class__.__name__, self.event)
            return None

        match = CONTACT_EMAIL_RE.match(self.contact_email)

        if not match:
            logger.warn('Invalid contact_email in %s for %s: %s',
                self.__class__.__name__,
                self.event,
                self.contact_email,
            )
            return None

        return match

    @property
    def plain_contact_email(self):
        match = self.match_contact_email()
        if match:
            return match.group('email')
        else:
            return ''

    @property
    def cloaked_plain_contact_email(self):
        from access.models import InternalEmailAlias
        app_label = self._meta.app_label
        alias = InternalEmailAlias.objects.get(app_label=app_label, event=self.event)
        return alias.email_address

    @property
    def cloaked_contact_email(self):
        match = self.match_contact_email()
        if match:
            return '{name} <{email}>'.format(
                name=match.group('name'),
                email=self.cloaked_plain_contact_email
            )
        else:
            return self.cloaked_plain_contact_email
