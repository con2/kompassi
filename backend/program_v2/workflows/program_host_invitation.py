from dimensions.utils.dimension_cache import DimensionCache
from forms.models.response import Response
from forms.models.workflow import Workflow


class ProgramHostInvitationWorkflow(Workflow):
    """
    Note that the Universe for program host invitations is the Involvement universe.

    XXX This Workflow is silly because everything is handled in accept_invitation.py.
    """

    def ensure_involvement(self, response: Response, cache: DimensionCache):
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

    def handle_new_response_phase1(
        self,
        response: Response,
        old_version: Response | None = None,
    ):
        pass

    def handle_new_response_phase2(
        self,
        response: Response,
        old_version: Response | None = None,
    ):
        pass
