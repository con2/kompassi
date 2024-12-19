import graphene

from access.cbac import graphql_check_model
from core.models import Event

from ...models.quota import Quota
from ..quota_limited import LimitedQuotaType


class CreateQuotaInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    name = graphene.String(required=True)
    quota = graphene.Int(required=True)


class CreateQuota(graphene.Mutation):
    class Arguments:
        input = CreateQuotaInput(required=True)

    quota = graphene.Field(LimitedQuotaType)

    @staticmethod
    def mutate(
        root,
        info,
        input: CreateQuotaInput,
    ):
        event = Event.objects.get(slug=input.event_slug)
        graphql_check_model(Quota, event.scope, info, "mutation")

        quota = Quota(
            event=event,
            name=input.name,
        )
        quota.full_clean()
        quota.save()

        quota.set_quota(input.quota)  # type: ignore

        return CreateQuota(quota=quota)  # type: ignore
