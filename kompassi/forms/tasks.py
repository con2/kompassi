from django.tasks import task


@task
def response_notify_subscribers(response_id: str, old_version_id: str | None = None):
    from .models.response import Response

    response = Response.objects.get(id=response_id)
    old_version = Response.objects.get(id=old_version_id) if old_version_id else None

    response.survey.workflow._notify_subscribers(response, old_version)
