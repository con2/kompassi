from kompassi.dimensions.utils.dimension_cache import DimensionCache
from kompassi.forms.models.response import Response
from kompassi.forms.models.workflow import Workflow
from kompassi.involvement.models.involvement import Involvement

from ...forms.utils.extract_annotations import extract_annotations_from_responses


class ProgramHostInvitationWorkflow(Workflow):
    """
    Note that the Universe for program host invitations is the Involvement universe.

    XXX This Workflow is silly because everything is handled in accept_invitation.py.
    """

    def ensure_involvement(
        self,
        response: Response,
        *,
        old_version: Response | None = None,
        cache: DimensionCache,
    ):
        # NOTE rethink this
        # need Invitation to create Involvement
        # Furthermore, the accept_invitation mutation needs the Involvement
        # So it is now created there
        pass

    def ensure_survey_to_badge(self, response: Response):
        """
        The program host invitation workflow doesn't use STB.
        Badges are managed via Involvement.
        """
        return None, False

    def handle_new_response_phase2(
        self,
        response: Response,
        old_version: Response | None = None,
    ):
        involvement = Involvement.objects.get(
            program__isnull=False,
            response=response,
        )

        program = involvement.program
        if program is None:
            raise AssertionError("No it isn't (appease typechecker)")

        program.refresh_annotations(
            extract_annotations_from_responses(
                program.responses.all(),
                program.universe.active_universe_annotations.all(),
            )
        )
        program.refresh_dependents()
