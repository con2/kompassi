from celery import shared_task

from core.models import Person

from .models import Privilege, SMTPServer


@shared_task(ignore_result=True)
def grant_privilege(privilege_id, person_id):
    privilege = Privilege.objects.get(id=privilege_id)
    person = Person.objects.get(id=person_id)

    privilege._grant(person)


@shared_task(ignore_result=True)
def smtp_server_push_smtppasswd_file(smtp_server_id):
    smtp_server = SMTPServer.objects.get(id=smtp_server_id)
    smtp_server._push_smtppasswd_file()
