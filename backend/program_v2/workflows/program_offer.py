import logging

from access.cbac import is_graphql_allowed_for_model
from forms.models.response import Response
from forms.models.survey import Survey
from forms.models.workflow import Workflow
from tickets_v2.views.pos_view import HttpRequest

from ..dimensions import get_form_dimension_dto, setup_program_dimensions

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
