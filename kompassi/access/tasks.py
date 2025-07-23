from kompassi.celery_app import app

from .models import SMTPServer


@app.task(ignore_result=True)
def smtp_server_push_smtppasswd_file(smtp_server_id):
    smtp_server = SMTPServer.objects.get(id=smtp_server_id)
    smtp_server._push_smtppasswd_file()
