from enum import Enum

import graphene
from django.db import transaction
from django.http import HttpRequest

from access.cbac import graphql_check_instance
from core.models.event import Event
from event_log_v2.utils.emit import emit
from involvement.models.involvement import Involvement


class ProgramItemResolution(Enum):
    CANCEL = "cancel"
    CANCEL_AND_HIDE = "cancel_and_hide"
    DELETE = "delete"


ProgramItemResolutionType = graphene.Enum.from_enum(ProgramItemResolution)


class CancelProgramInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)
    resolution = graphene.Argument(ProgramItemResolutionType, required=True)


class CancelProgram(graphene.Mutation):
    class Arguments:
        input = CancelProgramInput(required=True)

    program_slug = graphene.NonNull(graphene.String)
    response_id = graphene.Field(
        graphene.UUID,
        description="If the program item was created from a program offer, this is the offer ID.",
    )

    @transaction.atomic
    @staticmethod
    def mutate(_root, info, input: CancelProgramInput):
        request: HttpRequest = info.context
        event = Event.objects.get(slug=input.event_slug)
        meta = event.program_v2_event_meta
        if not meta:
            raise ValueError("Event does not use Program V2")

        program = meta.programs.get(slug=input.program_slug)
        program_slug = program.slug
        response_id = program.program_offer_id

        # TODO(#671) cancel own program item (now only admin cancel is implemented)

        graphql_check_instance(
            program,
            info,
            app="program_v2",
            operation="delete",
        )

        program_dimensions_cache = meta.universe.preload_dimensions(["state"])
        involvement_dimensions_cache = program.event.involvement_universe.preload_dimensions()

        match input.resolution:
            case ProgramItemResolution.CANCEL:
                emit(
                    "program_v2.programs.cancelled",
                    request=request,
                    program=program_slug,
                    organization=event.organization,
                    event=program.event,
                )

                program.set_dimension_values(
                    {"state": ["cancelled"]},
                    cache=program_dimensions_cache,
                )
                program.refresh_cached_fields()
                Involvement.from_program_state_change(
                    program,
                    cache=involvement_dimensions_cache,
                )
                program.refresh_dependents()
            case ProgramItemResolution.DELETE:
                emit(
                    "program_v2.programs.deleted",
                    request=request,
                    program=program_slug,
                    organization=event.organization,
                    event=program.event,
                )

                Involvement.from_program_state_change(
                    program,
                    cache=involvement_dimensions_cache,
                    deleting=True,
                )

                program.delete()
            case _:
                raise NotImplementedError(f"Resolution {input.resolution} is not implemented")

        return CancelProgram(program_slug=program_slug, response_id=response_id)  # type: ignore
