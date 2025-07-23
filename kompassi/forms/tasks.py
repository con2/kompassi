from uuid import UUID

from kompassi.celery_app import app


@app.task(ignore_result=True)
def response_notify_subscribers(response_id: UUID, old_version_id: UUID | None = None):
    from .models.response import Response

    response = Response.objects.get(id=response_id)
    old_version = Response.objects.get(id=old_version_id) if old_version_id else None

    response.survey.workflow._notify_subscribers(response, old_version)
