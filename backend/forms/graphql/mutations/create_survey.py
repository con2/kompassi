import graphene

from access.cbac import graphql_check_model
from core.models import Event

from ...models.survey import Survey
from ..survey import SurveyType


class CreateSurveyInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)


class CreateSurvey(graphene.Mutation):
    class Arguments:
        input = CreateSurveyInput(required=True)

    survey = graphene.Field(SurveyType)

    @staticmethod
    def mutate(
        root,
        info,
        input: CreateSurveyInput,
    ):
        event = Event.objects.get(slug=input.event_slug)
        graphql_check_model(Survey, event, info, "mutation")
        survey = Survey(event=event, slug=input.survey_slug)
        survey.full_clean()  # Validate fields
        survey.save()
        return CreateSurvey(survey=survey)  # type: ignore
