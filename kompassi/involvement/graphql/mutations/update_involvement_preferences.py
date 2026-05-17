from datetime import datetime

import graphene
from django.utils.timezone import is_naive, make_aware

from kompassi.access.cbac import graphql_check_instance
from kompassi.involvement.graphql.meta import InvolvementEventMetaType
from kompassi.involvement.models.meta import InvolvementEventMeta


class UpdateInvolvementPreferencesInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    shirts_frozen_at = graphene.DateTime()


class UpdateInvolvementPreferences(graphene.Mutation):
    class Arguments:
        input = UpdateInvolvementPreferencesInput(required=True)

    preferences = graphene.Field(InvolvementEventMetaType)

    @staticmethod
    def mutate(
        _root,
        info,
        input: UpdateInvolvementPreferencesInput,
    ):
        meta = InvolvementEventMeta.objects.get(event__slug=input.event_slug)

        graphql_check_instance(
            meta,
            info,
            app="involvement",
            operation="update",
        )

        shirts_frozen_at: datetime | None = input.shirts_frozen_at  # type: ignore
        if shirts_frozen_at is not None and is_naive(shirts_frozen_at):
            shirts_frozen_at = make_aware(shirts_frozen_at)
        meta.shirts_frozen_at = shirts_frozen_at
        meta.save(update_fields=["shirts_frozen_at"])

        return UpdateInvolvementPreferences(preferences=meta)
