from celery import shared_task

from core.models import Person

from .models import Privilege


@shared_task(ignore_result=True)
def grant_privilege(privilege_id, person_id):
    privilege = Privilege.objects.get(id=privilege_id)
    person = Person.objects.get(id=person_id)

    privilege._grant(person)
