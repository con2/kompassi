import logging

from access.cbac import is_graphql_allowed_for_model
from core.models.event import Event
from dimensions.models.enums import DimensionApp
from forms.models.enums import Anonymity
from forms.models.response import Response
from forms.models.survey import Survey
from forms.models.workflow import Workflow
from involvement.dimensions import setup_involvement_dimensions
from involvement.models.involvement import Involvement
from tickets_v2.views.pos_view import HttpRequest

from ..dimensions import get_form_dimension_dto, get_program_universe, setup_program_dimensions
from ..models.program import Program
from ..models.schedule_item import ScheduleItem

logger = logging.getLogger("kompassi")


class ProgramOfferWorkflow(Workflow, arbitrary_types_allowed=True):
    """
    Survey response workflow for the program offer to program item pipeline.
    """

    survey: Survey

    @classmethod
    def _get_default_dimension_values(cls, survey: Survey) -> dict[str, list[str]]:
        return {
            "state": ["new"],
            "form": [survey.slug],
        }

    def handle_new_survey(self):
        super().handle_new_survey()
        setup_program_dimensions(self.survey.universe)

        self.survey.set_default_response_dimension_values(
            self._get_default_dimension_values(self.survey),
            self.survey.universe.preload_dimensions(),
        )
        self.survey.refresh_cached_default_dimensions()

    @classmethod
    def backfill(cls, event: Event):
        logger.info("Backfilling program V2 settings for event %s", event.slug)

        program_universe = get_program_universe(event)
        setup_program_dimensions(program_universe)
        program_cache = program_universe.preload_dimensions()

        meta = event.program_v2_event_meta
        if meta is None:
            raise ValueError("Event has no program_v2_event_meta")

        if not meta.default_registry:
            raise ValueError("Event has no default registry for program_v2")

        # Program form settings
        Survey.objects.filter(
            event=event,
            app_name=DimensionApp.PROGRAM_V2.value,
        ).update(
            anonymity=Anonymity.FULL_PROFILE.value,
            registry=meta.default_registry,
        )

        for offer_form in meta.program_offer_forms.all():
            offer_form.with_mandatory_fields().save()
            offer_form.set_default_response_dimension_values(
                cls._get_default_dimension_values(offer_form), program_cache
            )
            offer_form.refresh_cached_default_dimensions()

        # Program offer dimensions
        for program_offer in meta.current_program_offers.all():
            existing_values = program_offer.cached_dimensions
            values_to_set = {}

            if not existing_values.get("state", []):
                values_to_set["state"] = ["accepted"] if program_offer.programs.exists() else ["new"]
            if not existing_values.get("form", []):
                values_to_set["form"] = [program_offer.survey.slug]

            if values_to_set:
                program_offer.set_dimension_values(values_to_set, program_cache)

        # Program dimensions
        for program in Program.objects.filter(event=event):
            existing_values = program.cached_dimensions
            values_to_set = {}

            if not existing_values.get("state", []):
                values_to_set["state"] = ["accepted"]
            if not existing_values.get("form", []):
                values_to_set["form"] = [program.program_offer.survey.slug] if program.program_offer else []

            if values_to_set:
                program.set_dimension_values(values_to_set, program_cache)

        Program.refresh_cached_fields_qs(meta.programs.all(), cache=program_cache)
        ScheduleItem.refresh_cached_fields_qs(meta.schedule_items.all())

        # Involvements
        involvement_universe = event.involvement_universe
        setup_involvement_dimensions(involvement_universe, event)
        involvement_cache = involvement_universe.preload_dimensions()

        # Due to faulty logic, each version of a program offer generated an Involvement.
        _, deleted_by_model = Involvement.objects.filter(
            # Of this event
            universe=involvement_universe,
            # Is of type program offer (ie. not program host in a program item)
            program__isnull=True,
            # Is an old version of a program offer
            response__superseded_by__isnull=False,
            # Just to be sure: This version of the program offer has not been accepted as a program item
            response__programs__isnull=True,
        ).delete()
        logger.info("Involvement cleanup for old response versions deleted: %s", deleted_by_model)

        for program_offer in meta.current_program_offers.all():
            program_offer.survey.workflow.ensure_involvement(program_offer, cache=involvement_cache)

        for program in meta.programs.all():
            Involvement.from_program_state_change(
                program=program,
                cache=involvement_cache,
            )

        Program.refresh_cached_fields_qs(meta.programs.all(), cache=program_cache)

    def handle_form_update(self):
        """
        If form titles have changed, update them in the dimension.
        """
        universe = self.survey.universe
        get_form_dimension_dto(universe).save(universe)

    def is_response_active(self, response: Response) -> bool:
        return not bool(set(response.cached_dimensions.get("state", [])).intersection({"cancelled", "rejected"}))

    def ensure_survey_to_badge(self, response: Response):
        """
        The program offer workflow doesn't use STB.
        Badges are managed via Involvement.
        """
        return None, False

    def response_can_be_edited_by_owner(self, response: Response, request: HttpRequest) -> bool:
        # cannot use is_subject_locked on state=accepted because we may want to allow editing the program but not the offer
        return super().response_can_be_edited_by_owner(response, request) and "new" in response.cached_dimensions.get(
            "state", ["new"]
        )

    def response_can_be_accepted_by(
        self,
        response: Response,
        request: HttpRequest,
    ) -> bool:
        """
        A program offer can be accepted multiple times.
        A rejected or cancelled offer can be accepted again, turning it into an accepted offer.
        Old versions of the response are handled when the current version is accepted.
        """
        return response.is_current_version

    def response_can_be_cancelled_by(
        self,
        response: Response,
        request: HttpRequest,
    ) -> bool:
        """
        Cancelling a program offer that has already been accepted only makes sense
        when all the programs have been cancelled or rejected. This is done via
        program item admin and not via the program offer workflow.

        Cancelling or rejecting a cancelled program offer merely changes its state,
        so this is allowed to let the program admin change their mind about whether
        the program offer should be considered cancelled or rejected.

        Old versions of the response are handled when the current version is cancelled.
        """
        return response.is_current_version and is_graphql_allowed_for_model(
            request.user,
            instance=response.survey,
            app="program_v2",
            operation="delete",
            field="responses",
        )
