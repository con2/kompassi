import graphene
from django.db import transaction
from django.http import HttpRequest

from core.models import Event

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
        event = Event.objects.get(slug=input.event_slug)
        quota = Quota.objects.get(event=event, id=input.quota_id)

        request: HttpRequest = info.context
        if not quota.can_be_deleted_by(request):
            raise ValueError("Cannot delete quota")

        quota.delete()

        return DeleteQuota(id=input.quota_id)  # type: ignore
