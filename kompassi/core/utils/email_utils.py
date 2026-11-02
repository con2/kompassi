import logging

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def send_email_message(**opts):
    if settings.DEBUG:
        logger.debug(opts["body"])

    EmailMessage(**opts).send()
