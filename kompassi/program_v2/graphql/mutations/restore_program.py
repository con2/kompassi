import graphene
from django.db import transaction
from django.http import HttpRequest

from kompassi.core.models.event import Event
from kompassi.event_log_v2.utils.emit import emit
from kompassi.involvement.models.involvement import Involvement


class RestoreProgramInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_slug = graphene.String(required=True)


class RestoreProgram(graphene.Mutation):
    """
    Restore a program item that was previously cancelled.
    """

    class Arguments:
        input = RestoreProgramInput(required=True)

    program_slug = graphene.NonNull(graphene.String)

    @transaction.atomic
    @staticmethod
    def mutate(_root, info, input: RestoreProgramInput):
        request: HttpRequest = info.context
        event = Event.objects.get(slug=input.event_slug)
        meta = event.program_v2_event_meta
        if not meta:
            raise ValueError("Event does not use Program V2")

        program = meta.programs.get(slug=input.program_slug)
        program_slug = program.slug

        if not program.can_be_restored_by(request):
            raise ValueError("You cannot restore this program.")

        program_dimensions_cache = meta.universe.preload_dimensions()
        involvement_dimensions_cache = program.event.involvement_universe.preload_dimensions()

        emit(
            "program_v2.programs.restored",
            request=request,
            program=program_slug,
            organization=event.organization,
            event=program.event,
        )

        program.set_dimension_values(
            {"state": ["accepted"]},
            cache=program_dimensions_cache,
        )
        program.refresh_cached_fields()
        Involvement.from_program_state_change(
            program,
            cache=involvement_dimensions_cache,
        )
        program.refresh_dependents()

        if program_offer := program.program_offer:
            program_offer.set_dimension_values(program.cached_dimensions, cache=program_dimensions_cache)
            program_offer.refresh_cached_fields()
            program_offer.survey.workflow.handle_response_dimension_update(program_offer)

        return RestoreProgram(program_slug=program_slug)  # type: ignore
