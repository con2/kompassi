import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.tasks import task

logger = logging.getLogger(__name__)


@task
def send_email(**opts):
    if settings.DEBUG:
        logger.debug(opts["body"])

    EmailMessage(**opts).send(fail_silently=False)
