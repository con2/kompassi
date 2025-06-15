from enum import Enum

import graphene
from django.db import transaction
from django.http import HttpRequest

from access.cbac import graphql_check_instance
from core.models.event import Event
from event_log_v2.utils.emit import emit
from involvement.models.involvement import Involvement


class ProgramOfferResolution(Enum):
    REJECT = "reject"
    CANCEL = "cancel"
    DELETE = "delete"


ProgramOfferResolutionType = graphene.Enum.from_enum(ProgramOfferResolution)


class CancelProgramOfferInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    response_id = graphene.UUID(required=True)
    resolution = graphene.Argument(ProgramOfferResolutionType, required=True)


class CancelProgramOffer(graphene.Mutation):
    class Arguments:
        input = CancelProgramOfferInput(required=True)

    response_id = graphene.NonNull(graphene.UUID)

    @transaction.atomic
    @staticmethod
    def mutate(_root, info, input: CancelProgramOfferInput):
        request: HttpRequest = info.context
        event = Event.objects.get(slug=input.event_slug)
        meta = event.program_v2_event_meta
        if not meta:
            raise ValueError("Event does not use Program V2")

        program_offer = meta.current_program_offers.get(id=input.response_id)
        response_id = program_offer.id

        # TODO(#670) cancel own program offer (now only admin cancel is implemented)

        graphql_check_instance(
            program_offer,
            info,
            app="program_v2",
            operation="delete",
        )

        program_dimensions_cache = program_offer.survey.universe.preload_dimensions(["state"])
        involvement_dimensions_cache = program_offer.event.involvement_universe.preload_dimensions()

        match input.resolution:
            case ProgramOfferResolution.REJECT:
                program_offer.set_dimension_values(
                    {"state": ["rejected"]},
                    cache=program_dimensions_cache,
                )
                program_offer.refresh_cached_fields()
                Involvement.from_survey_response(
                    program_offer,
                    cache=involvement_dimensions_cache,
                )
            case ProgramOfferResolution.CANCEL:
                program_offer.set_dimension_values(
                    {"state": ["cancelled"]},
                    cache=program_dimensions_cache,
                )
                program_offer.refresh_cached_fields()
                Involvement.from_survey_response(
                    program_offer,
                    cache=involvement_dimensions_cache,
                )
            case ProgramOfferResolution.DELETE:
                emit(
                    "forms.response.deleted",
                    request=request,
                    response=program_offer,
                    organization=event.organization,
                    event=program_offer.event,
                )

                Involvement.from_survey_response(
                    program_offer,
                    cache=involvement_dimensions_cache,
                    deleting=True,
                )

                meta.all_program_offers.filter(superseded_by=program_offer).delete()
                program_offer.delete()
            case _:
                raise NotImplementedError(f"Resolution {input.resolution} is not implemented")

        return CancelProgramOffer(response_id=response_id)  # type: ignore
