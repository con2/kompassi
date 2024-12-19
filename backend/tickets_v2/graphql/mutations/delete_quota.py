import graphene

from access.cbac import graphql_check_instance
from core.models import Event

from ...models.quota import Quota
from ..quota_limited import LimitedQuotaType


class DeleteQuotaInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    quota_id = graphene.Int(required=True)


class DeleteQuota(graphene.Mutation):
    class Arguments:
        input = DeleteQuotaInput(required=True)

    quota = graphene.Field(LimitedQuotaType)

    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteQuotaInput,
    ):
        event = Event.objects.get(slug=input.event_slug)
        quota = Quota.objects.get(event=event, id=input.quota_id)
        graphql_check_instance(quota, info, "self", "delete")

        # TODO can_delete
        if quota.products.exists():
            raise ValueError("Cannot delete quota with products")

        quota.delete()

        return DeleteQuota(quota=quota)  # type: ignore
