import graphene
from django.http import HttpRequest

from kompassi.core.models.person import Person

from ...models.survey import Survey
from ..survey_full import FullSurveyType


class SurveyAccessInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    person_id = graphene.Int(required=True)


class GrantSurveyAccess(graphene.Mutation):
    class Arguments:
        input = SurveyAccessInput(required=True)

    survey = graphene.Field(FullSurveyType)

    @staticmethod
    def mutate(
        root,
        info,
        input: SurveyAccessInput,
    ):
        request: HttpRequest = info.context
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        workflow = survey.workflow

        if not workflow.can_access_be_granted:
            raise ValueError("Access cannot be granted per survey for this survey")

        workflow.check_access(info, operation="create", field="access")

        person = Person.objects.get(id=input.person_id)
        workflow.grant_access(person, request)

        return GrantSurveyAccess(survey=survey)  # type: ignore


class RevokeSurveyAccess(graphene.Mutation):
    class Arguments:
        input = SurveyAccessInput(required=True)

    survey = graphene.Field(FullSurveyType)

    @staticmethod
    def mutate(
        root,
        info,
        input: SurveyAccessInput,
    ):
        request: HttpRequest = info.context
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        workflow = survey.workflow

        if not workflow.can_access_be_granted:
            raise ValueError("Access cannot be granted per survey for this survey")

        workflow.check_access(info, operation="delete", field="access")

        person = Person.objects.get(id=input.person_id)
        workflow.revoke_access(person, request)

        return RevokeSurveyAccess(survey=survey)  # type: ignore
