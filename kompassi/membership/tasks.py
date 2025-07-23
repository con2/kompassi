from kompassi.celery_app import app

from .models import Membership


@app.task(ignore_result=True)
def membership_apply_state(membership_id):
    membership = Membership.objects.get(id=membership_id)
    membership._apply_state()
