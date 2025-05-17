from dimensions.utils.dimension_cache import DimensionCache
from forms.models.response import Response
from forms.models.workflow import Workflow


class ProgramHostInvitationWorkflow(Workflow):
    """
    Note that the Universe for program host invitations is the Involvement universe.
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
