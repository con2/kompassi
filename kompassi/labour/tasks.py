from kompassi.celery_app import app


@app.task(ignore_result=True)
def signup_apply_state(signup_pk):
    from .models import Signup

    signup = Signup.objects.get(pk=signup_pk)
    signup._apply_state()


@app.task(ignore_result=True)
def labour_event_meta_create_groups(meta_pk):
    from .models import LabourEventMeta

    meta = LabourEventMeta.objects.get(pk=meta_pk)
    meta.create_groups()
