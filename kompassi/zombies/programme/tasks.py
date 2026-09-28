from django.tasks import task


@task(max_attempts=3)
def programme_apply_state_async(programme_pk):
    from .models import Programme

    programme = Programme.objects.get(pk=programme_pk)
    programme._apply_state_async()
