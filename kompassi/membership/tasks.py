from django.tasks import task

from .models import Membership


@task(max_attempts=3)
def membership_apply_state(membership_id):
    membership = Membership.objects.get(id=membership_id)
    membership._apply_state()
