import graphene
from django.db import transaction
from django.http import HttpRequest

from kompassi.core.models import Event
from kompassi.event_log_v2.utils.emit import emit

from ...models.quota import Quota


class DeleteQuotaInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    quota_id = graphene.String(required=True)


class DeleteQuota(graphene.Mutation):
    class Arguments:
        input = DeleteQuotaInput(required=True)

    id = graphene.NonNull(graphene.String)

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteQuotaInput,
    ):
        request: HttpRequest = info.context

        event = Event.objects.get(slug=input.event_slug)
        quota = Quota.objects.get(event=event, id=input.quota_id)

        if not quota.can_be_deleted_by(request):
            raise ValueError("Cannot delete quota")

        quota.delete()

        emit(
            "tickets_v2.quota.deleted",
            event=event,
            quota=input.quota_id,
            request=request,
            context=quota.admin_url,
        )

        return DeleteQuota(id=input.quota_id)  # type: ignore
