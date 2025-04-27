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
                from program_v2.workflow import ProgramOfferWorkflow

                return ProgramOfferWorkflow(survey=survey)
            case _:
                return cls(survey=survey)

    def handle_form_update(self):
        """
        Called when a form of a survey using this workflow is created, deleted or updated.
        Not called for form field updates.
        """
        pass

    def handle_new_response_phase1(self, response: Response):
        """
        Called when a new response is created for a survey using this workflow.
        This is called during the transaction that creates the response.
        Do not call external services or perform any actions that require the transaction to be committed.
        """
        response.set_initial_dimension_values()
        response.lift_dimension_values()
        response.refresh_cached_dimensions()

    def handle_new_response_phase2(self, response: Response):
        """
        Called when a new response is created for a survey using this workflow.
        This is called after the transaction that creates the response is committed.
        This is the place to call external services or perform any actions that require the transaction to be committed.
        """
        response.notify_subscribers()
