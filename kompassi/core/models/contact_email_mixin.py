import logging
import re

from django.core.validators import RegexValidator

logger = logging.getLogger(__name__)

CONTACT_EMAIL_RE = re.compile(r"(?P<name>.+) <(?P<email>.+@.+\..+)>")
contact_email_validator = RegexValidator(CONTACT_EMAIL_RE)


class ContactEmailMixin:
    def match_contact_email(self):
        if not self.contact_email:  # type: ignore
            logger.warning("%s for %s has no contact_email", self.__class__.__name__, self.event)  # type: ignore
            return None

        match = CONTACT_EMAIL_RE.match(self.contact_email)  # type: ignore

        if not match:
            logger.warning(
                "Invalid contact_email in %s for %s: %s",
                self.__class__.__name__,
                self.event,  # type: ignore
                self.contact_email,  # type: ignore
            )
            return None

        return match

    @property
    def plain_contact_email(self) -> str:
        match = self.match_contact_email()
        if match:
            return match.group("email")
        else:
            return ""

    @property
    def cloaked_plain_contact_email(self) -> str:
        from kompassi.access.models import InternalEmailAlias

        app_label = self._meta.app_label  # type: ignore
        alias = InternalEmailAlias.objects.filter(app_label=app_label, event=self.event).order_by("-id").first()  # type: ignore

        if not alias:
            logger.warning("No internal alias found for %s in event %s", app_label, self.event)  # type: ignore
            return self.plain_contact_email

        return alias.email_address  # type: ignore

    @property
    def cloaked_contact_email(self) -> str:
        match = self.match_contact_email()
        if match:
            return f"{match.group('name')} <{self.cloaked_plain_contact_email}>"
        else:
            return self.cloaked_plain_contact_email
