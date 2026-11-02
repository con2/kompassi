from django.tasks import task

from .utils.email_utils import send_email_message

# these are separate tasks to identify the error path in case of a failed send


@task
def send_password_reset_email(**opts):
    send_email_message(**opts)


@task
def send_email_verification_email(**opts):
    send_email_message(**opts)
