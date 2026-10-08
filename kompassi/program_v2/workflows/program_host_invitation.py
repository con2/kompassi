from kompassi.dimensions.utils.dimension_cache import DimensionCache
from kompassi.forms.models.response import Response
from kompassi.forms.models.workflow import Workflow
from kompassi.involvement.models.involvement import Involvement

from ...forms.utils.extract_annotations import extract_annotations_from_responses
from ...forms.utils.extract_dimension_values import extract_dimension_values_for_universe


class ProgramHostInvitationWorkflow(Workflow):
    """
    Program host invitations created after the Involvement universe became their home live in it;
    older ones (see Survey.is_in_involvement_universe) still live in the program universe.

    XXX This Workflow is silly because everything is handled in accept_invitation.py.
    """

    @property
    def access_root_claims(self):
        """
        Program forms are governed by event-wide program_v2 admin rights and
        cannot be granted access to on a per-survey basis.
        """
        return {}

    @property
    def protect_responses(self) -> bool:
        """
        Program form responses are protected by the event-wide ProgramV2EventMeta.protect_responses
        switch instead of Survey.protect_responses.
        """
        meta = self.survey.event.program_v2_event_meta
        return meta is None or meta.protect_responses

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

        # Fields that describe the host were passed forward to the Involvement in
        # Involvement.from_accepted_invitation. Fields that describe the program item,
        # ie. those in the program universe, pass forward here.
        on_edit = old_version is not None
        program_cache = program.universe.preload_dimensions()

        program.refresh_annotations(
            extract_annotations_from_responses(
                program.responses.all(),
                program.universe.active_universe_annotations.all(),
                on_edit=on_edit,
            )
        )

        dimension_values = extract_dimension_values_for_universe(response, cache=program_cache, on_edit=on_edit)
        if dimension_values:
            program.set_dimension_values(dimension_values, cache=program_cache)
            program.refresh_cached_fields()

        program.refresh_dependents()
