from enum import Enum

import graphene
from django.db import transaction

from access.cbac import graphql_check_instance
from core.models.event import Event


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

    response_id = graphene.UUID()

    @transaction.atomic
    @staticmethod
    def mutate(_root, info, input: CancelProgramOfferInput):
        event = Event.objects.get(slug=input.event_slug)
        meta = event.program_v2_event_meta
        if not meta:
            raise ValueError("Event is not a program event")

        program_offer = meta.current_program_offers.get(id=input.response_id)

        # TODO(#670) cancel own program offer (now only admin cancel is implemented)

        graphql_check_instance(
            program_offer,
            info,
            app="program_v2",
            operation="delete",
        )

        cache = program_offer.survey.universe.preload_dimensions(["state"])

        match input.resolution:
            case ProgramOfferResolution.REJECT:
                program_offer.set_dimension_values({"state": ["rejected"]}, cache)
                program_offer.refresh_cached_fields()
            case ProgramOfferResolution.CANCEL:
                program_offer.set_dimension_values({"state": ["cancelled"]}, cache)
                program_offer.refresh_cached_fields()
            case ProgramOfferResolution.DELETE:
                program_offer.delete()
            case _:
                raise NotImplementedError(f"Resolution {input.resolution} is not implemented")

        return CancelProgramOffer(response_id=program_offer.id)  # type: ignore
