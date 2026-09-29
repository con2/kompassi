from django.tasks import task


@task
def privileges_form_save(event_id, data):
    from django.contrib.auth import get_user_model

    from kompassi.core.models import Event

    from .forms import PrivilegesForm

    User = get_user_model()
    event = Event.objects.get(id=event_id)
    data = [(User.objects.get(id=user_id), cleaned_data) for (user_id, cleaned_data) in data]
    PrivilegesForm._save(event, data)  # type: ignore
