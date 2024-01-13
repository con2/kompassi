import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management import call_command

logger = logging.getLogger("kompassi")


@shared_task(ignore_result=True)
def send_email(**opts):
    if settings.DEBUG:
        logger.debug(opts["body"])

    EmailMessage(**opts).send(fail_silently=False)


@shared_task(ignore_result=True)
def run_admin_command(*args, **kwargs):
    call_command(*args, **kwargs)
