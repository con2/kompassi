from django.tasks import task

from .utils.email_utils import send_email_message


@task
def send_password_reset_email(**opts):
    send_email_message(**opts)


@task
def send_email_verification_email(**opts):
    send_email_message(**opts)


@task
def send_email(**opts):
    """
    Deprecated: only runs jobs enqueued under this path before the per-use-case tasks
    existed. Remove once none are left in the queue. Do not enqueue new jobs here.
    """
    send_email_message(**opts)
