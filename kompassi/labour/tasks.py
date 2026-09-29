from django.tasks import task


@task(max_attempts=3)
def signup_apply_state(signup_pk):
    from .models import Signup

    signup = Signup.objects.get(pk=signup_pk)
    signup._apply_state()


@task
def labour_event_meta_create_groups(meta_pk):
    from .models import LabourEventMeta

    meta = LabourEventMeta.objects.get(pk=meta_pk)
    meta.create_groups()
