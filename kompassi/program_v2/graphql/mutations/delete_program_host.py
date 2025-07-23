import logging

import graphene
from django.db import transaction
from django.http import HttpRequest

from kompassi.access.cbac import graphql_check_instance

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

        graphql_check_instance(
            program,
            request,
            field="program_hosts",
            operation="delete",
        )

        with transaction.atomic():
            involvement = program.active_program_hosts.select_for_update(of=("self",), no_key=True).get(
                id=input.involvement_id,
            )
            involvement.is_active = False
            involvement.save(update_fields=["is_active"])
            involvement.refresh_dependents()

            # TODO(#728) Soft delete of program hosts
            # At the moment we can't distinguish soft delete from cancelled program
            # using is_active alone, so we just delete the program host involvement.
            involvement.delete()

        return DeleteProgramHost(program=program)  # type: ignore
