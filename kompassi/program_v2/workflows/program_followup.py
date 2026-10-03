from django.http import HttpRequest

from kompassi.dimensions.utils.dimension_cache import DimensionCache
from kompassi.forms.models.response import Response
from kompassi.forms.models.workflow import Workflow
from kompassi.forms.utils.extract_annotations import extract_annotations_from_responses
from kompassi.forms.utils.extract_dimension_values import extract_dimension_values_from_response
from kompassi.involvement.models.enums import InvolvementType
from kompassi.involvement.models.involvement import Involvement

from .program_host_invitation import ProgramHostInvitationWorkflow


class ProgramFollowupWorkflow(ProgramHostInvitationWorkflow):
    """
    Asks program hosts for more information after their program offers have been accepted.

    Responses are about the host, not a specific program item. They create no Involvement:
    values are passed forward to the respondent's existing PROGRAM_HOST involvements.
    Shares the access and badge rules of host invitations, which are the other form of
    information collected from program hosts.
    """

    def can_be_responded_by(self, request: HttpRequest) -> bool:
        user = request.user
        if not user.is_authenticated:
            return False

        person = getattr(user, "person", None)
        if person is None:
            return False

        return self._program_host_involvements(person).exists()

    def response_can_be_edited_by_owner(self, response: Response, request: HttpRequest) -> bool:
        # the owner may have stopped being a program host since responding
        return self.can_be_responded_by(request) and super().response_can_be_edited_by_owner(response, request)

    def _program_host_involvements(self, person):
        return self.survey.event.involvements.filter(
            person=person,
            type=InvolvementType.PROGRAM_HOST,
            is_active=True,
        )

    def ensure_involvement(
        self,
        response: Response,
        *,
        old_version: Response | None = None,
        cache: DimensionCache,
        override_dimensions: bool = False,
        on_edit: bool | None = None,
    ) -> Involvement | None:
        """
        :param on_edit: Whether to pass forward the values marked for edits instead of those marked for creation.
            Inferred from old_version if not given.
        """
        respondent = response.original_created_by
        person = getattr(respondent, "person", None)
        if person is None:
            return None

        if on_edit is None:
            on_edit = old_version is not None

        dimensions = extract_dimension_values_from_response(response, on_edit=on_edit)
        annotations = extract_annotations_from_responses(
            [response],
            cache.universe.active_universe_annotations.all(),
            on_edit=on_edit,
        )

        for involvement in self._program_host_involvements(person):
            involvement.annotations = {**involvement.annotations, **annotations}
            involvement.save(update_fields=["annotations"])
            if dimensions:
                involvement.refresh_dimensions(dimensions, cache=cache)
            involvement.refresh_dependents()

        return None

    def handle_response_dimension_update(self, response: Response):
        self.ensure_involvement(
            response,
            cache=response.event.involvement_universe.preload_dimensions(),
            on_edit=True,
        )
        self.ensure_survey_to_badge(response)

    def handle_new_response_phase2(
        self,
        response: Response,
        old_version: Response | None = None,
    ):
        # Skips the parent's refresh of program annotations: values were passed forward in ensure_involvement.
        Workflow.handle_new_response_phase2(self, response, old_version)
