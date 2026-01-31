import graphene
from django.db import transaction
from django.http import HttpRequest

from kompassi.core.models.event import Event
from kompassi.event_log_v2.utils.emit import emit
from kompassi.involvement.models.enums import InvolvementApp, InvolvementType
from kompassi.involvement.models.involvement import Involvement


class DeleteProgramOffersInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    program_offer_ids = graphene.List(graphene.String)


class DeleteProgramOffers(graphene.Mutation):
    class Arguments:
        input = DeleteProgramOffersInput(required=True)

    count_deleted = graphene.NonNull(graphene.Int)

    @transaction.atomic
    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteProgramOffersInput,
    ):
        request: HttpRequest = info.context

        event = Event.objects.get(slug=input.event_slug)
        meta = event.program_v2_event_meta
        if meta is None:
            raise ValueError("Event does not have program V2 meta")

        if not meta.can_program_offers_be_deleted_by(request):
            raise ValueError("Cannot delete program offers")

        program_offer_ids: set[str] = set(input.program_offer_ids)  # type: ignore
        if len(input.program_offer_ids) != len(program_offer_ids):  # type: ignore
            raise ValueError("Duplicate program offer IDs provided")

        program_offers = meta.current_program_offers.filter(id__in=program_offer_ids)
        if program_offers.count() != len(program_offer_ids):
            raise ValueError("Some program offers not found")

        old_versions = meta.all_program_offers.filter(superseded_by__in=program_offer_ids)
        old_version_ids = set(old_versions.values_list("id", flat=True))

        # We let the delete cascade to PROGRAM_OFFER involvements
        # But we want to spare the PROGRAM_HOST involvements
        Involvement.objects.filter(
            universe=event.involvement_universe,
            app=InvolvementApp.PROGRAM,
            type=InvolvementType.PROGRAM_HOST,
            response__in=program_offer_ids.union(old_version_ids),
        ).update(response=None)

        _, deleted_by_model = old_versions.delete()
        count_deleted = deleted_by_model.get("forms.Response", 0)

        _, deleted_by_model = program_offers.delete()
        count_deleted += deleted_by_model.get("forms.Response", 0)

        emit(
            "program_v2.program_offer.deleted",
            request=request,
            organization=event.organization.slug,
            event=event.slug,
            count_deleted=count_deleted,
        )

        return DeleteProgramOffers(count_deleted=count_deleted)  # type: ignore
