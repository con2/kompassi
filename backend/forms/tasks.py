from uuid import UUID

from celery import shared_task


@shared_task(ignore_result=True)
def response_notify_subscribers(response_id: UUID):
    from .models.response import Response

    response = Response.objects.get(id=response_id)
    response.survey.workflow._notify_subscribers(response)
