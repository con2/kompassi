from django.tasks import task

from .models import SMTPServer


@task
def smtp_server_push_smtppasswd_file(smtp_server_id):
    smtp_server = SMTPServer.objects.get(id=smtp_server_id)
    smtp_server._push_smtppasswd_file()
