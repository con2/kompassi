from kompassi.celery_app import app


@app.task(ignore_result=True)
def programme_apply_state_async(programme_pk):
    from .models import Programme

    programme = Programme.objects.get(pk=programme_pk)
    programme._apply_state_async()
