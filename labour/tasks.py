from __future__ import absolute_import

from celery import shared_task


@shared_task(ignore_result=True)
def signup_apply_state(signup_pk):
    from .models import Signup
    signup = Signup.objects.get(pk=signup_pk)
    signup._apply_state()