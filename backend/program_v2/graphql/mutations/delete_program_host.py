import logging

import graphene
from django.db import transaction
from django.http import HttpRequest

from access.cbac import graphql_check_instance
from badges.models import Badge

from ...models.program import Program
from ..program_full import FullProgramType

logger = logging.getLogger(__name__)


class DeleteProgramHostInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)
    involvement_id = graphene.String(required=True)


class DeleteProgramHost(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(DeleteProgramHostInput)

    program = graphene.NonNull(FullProgramType)

    def mutate(self, info, input):
        request: HttpRequest = info.context
        program = Program.objects.get(event__slug=input.event_slug, slug=input.program_slug)
        event = program.event

        graphql_check_instance(
            program,
            request,
            field="program_hosts",
            operation="delete",
        )

        with transaction.atomic():
            involvement = program.program_hosts.select_for_update().get(id=input.involvement_id)
            involvement.is_active = False
            involvement.save(update_fields=["is_active"])

            program.refresh_cached_fields()
            Badge.ensure(event, involvement.person)

        return DeleteProgramHost(program=program)  # type: ignore
