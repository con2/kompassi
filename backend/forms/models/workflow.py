import pydantic

from .response import Response
from .survey import Survey, SurveyApp


class Workflow(pydantic.BaseModel, arbitrary_types_allowed=True):
    """
    Workflow model for the form builder. The workflow defines
    a state dimension that is updated automatically at certain
    points in the workflow, and possibly some other automated
    actions in the future.

    We start with code-only, basic workflows such as

    - for basic surveys, nothing special is done
    - for program offers, some dimension values are set

    These may at some point be realized into the database.
    """

    survey: Survey

    @property
    def app(self) -> SurveyApp:
        return SurveyApp(self.survey.app)

    @classmethod
    def get_workflow(cls, survey: Survey):
        match SurveyApp(survey.app):
            case SurveyApp.PROGRAM_V2:
                from program_v2.workflow import ProgramWorkflow

                return ProgramWorkflow(survey=survey)
            case _:
                return cls(survey=survey)

    def is_response_active(self, response: Response) -> bool:
        # The basic survey workflow does not have a concept of active/inactive responses.
        return True

    def handle_new_survey(self):
        """
        Called when a new form is created for a survey using this workflow.
        """
        pass

    def handle_form_update(self):
        """
        Called when a form of a survey using this workflow is created, deleted or updated.
        Not called for form field updates.
        """
        pass

    def handle_new_response_phase1(self, response: Response):
        """
        Called when a new response is created for a survey using this workflow.
        Called during the transaction that creates the response.
        Do not call external services or perform any actions that require the transaction to be committed.
        """
        cache = self.survey.universe.preload_dimensions()
        response.set_dimension_values(self.survey.cached_default_dimensions, cache=cache)
        response.lift_dimension_values(cache=cache)
        response.refresh_cached_dimensions()

        self.ensure_involvement(response)

        return cache

    def handle_new_response_phase2(self, response: Response):
        """
        Called when a new response is created for a survey using this workflow.
        Called after the transaction that creates the response is committed.
        This is the place to call external services or perform any actions that require the transaction to be committed.
        """
        response.notify_subscribers()
        self.ensure_badges(response)

    def handle_response_dimension_update(self, response: Response):
        """
        Called when dimension values of a response are updated.
        Called after the transaction that updates the response dimensions is committed.
        Not called for newly created responses.
        """
        self.ensure_involvement(response)
        self.ensure_badges(response)

    def ensure_involvement(self, response: Response):
        """
        If the response ought to result in Involvement, create it.
        """
        from involvement.models.involvement import Involvement

        if not response.survey.registry:
            return

        Involvement.from_survey_response(
            response=response,
            cache=response.event.involvement_universe.preload_dimensions(),
        )

    def ensure_badges(self, response: Response):
        """
        Invoke Survey to Badge (STB) for new responses.
        See https://outline.con2.fi/doc/survey-to-badge-stb-mxK1UW6hAn
        """
        from badges.models.badge import Badge
        from badges.models.survey_to_badge import SurveyToBadgeMapping

        if not SurveyToBadgeMapping.objects.filter(survey=response.survey).exists():
            return None, False

        user = response.created_by
        if not user or not user.person:
            return None, False

        return Badge.ensure(response.survey.event, user.person)
