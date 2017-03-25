

from celery import shared_task

from .models import Membership


@shared_task(ignore_result=True)
def membership_apply_state(membership_id):
    membership = Membership.objects.get(id=membership_id)
    membership._apply_state()