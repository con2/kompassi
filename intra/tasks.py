from celery import shared_task


@shared_task(ignore_result=True)
def privileges_form_save(event_id, user_id, cleaned_data):
    from core.models import Event
    from django.contrib.auth import get_user_model
    from .forms import PrivilegesForm

    User = get_user_model()
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=user_id)

    PrivilegesForm._save(event, user, cleaned_data)
