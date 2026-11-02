from django.tasks import task

from kompassi.core.utils.email_utils import send_email_message


@task
def send_desuprofile_confirmation_email(**opts):
    send_email_message(**opts)
