# encoding: utf-8

from __future__ import unicode_literals

import re
import logging

from django.core.validators import RegexValidator


logger = logging.getLogger('kompassi')

CONTACT_EMAIL_RE = re.compile(r'(?P<name>.+) <(?P<email>.+@.+\..+)>')
contact_email_validator = RegexValidator(CONTACT_EMAIL_RE)


class ContactEmailMixin(object):
    @property
    def plain_contact_email(self):
        if not self.contact_email:
            logger.warn('%s for %s has no contact_email', self.__class__.__name__, self.event)
            return ''

        match = CONTACT_EMAIL_RE.match(self.contact_email)

        if not match:
            logger.warn('Invalid contact_email in %s for %s: %s',
                self.__class__.__name__,
                self.event,
                self.contact_email,
            )
            return ''

        return match.group('email')
