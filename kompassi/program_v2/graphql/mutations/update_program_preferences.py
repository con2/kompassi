from datetime import datetime

import graphene
from django.utils.timezone import is_naive, make_aware

from kompassi.access.cbac import graphql_check_instance
from kompassi.program_v2.graphql.meta import ProgramV2EventMetaType
from kompassi.program_v2.models.meta import ProgramV2EventMeta


class UpdateProgramPreferencesInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    public_from = graphene.DateTime()


class UpdateProgramPreferences(graphene.Mutation):
    class Arguments:
        input = UpdateProgramPreferencesInput(required=True)

    preferences = graphene.Field(ProgramV2EventMetaType)

    @staticmethod
    def mutate(
        _root,
        info,
        input: UpdateProgramPreferencesInput,
    ):
        meta = ProgramV2EventMeta.objects.get(event__slug=input.event_slug)

        graphql_check_instance(
            meta,
            info,
            app="program_v2",
            operation="update",
        )

        public_from: datetime | None = input.public_from  # type: ignore
        if public_from is not None and is_naive(public_from):
            public_from = make_aware(public_from)
        meta.public_from = public_from
        meta.save(update_fields=["public_from"])

        return UpdateProgramPreferences(preferences=meta)
