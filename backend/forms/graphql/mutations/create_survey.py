import graphene
from django.http import HttpRequest

from access.cbac import graphql_check_instance, graphql_check_model
from core.models import Event
from dimensions.models.enums import DimensionApp

from ...models.enums import SurveyPurpose
from ...models.survey import Anonymity, Survey
from ..survey_full import FullSurveyType
from ..survey_limited import AnonymiType


class CreateSurveyInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    copy_from = graphene.String()
    anonymity = graphene.InputField(AnonymiType, required=True)


class CreateSurvey(graphene.Mutation):
    class Arguments:
        input = CreateSurveyInput(required=True)

    survey = graphene.Field(FullSurveyType)

    @staticmethod
    def mutate(
        root,
        info,
        input: CreateSurveyInput,
    ):
        # TODO scope
        event = Event.objects.get(slug=input.event_slug)
        request: HttpRequest = info.context

        graphql_check_model(
            Survey,
            event.scope,
            info,
            operation="create",
            app="forms",  # program offer forms created via another mutation
        )

        app = DimensionApp.FORMS
        purpose = SurveyPurpose.DEFAULT

        anonymity = Anonymity(input.anonymity)
        if input.copy_from:
            source_event_slug, source_survey_slug = str(input.copy_from).split("/")
            source_survey = Survey.objects.get(
                event__slug=source_event_slug,
                slug=source_survey_slug,
            )

            graphql_check_instance(
                source_survey,
                info,
                app=source_survey.app_name,  # NOTE same check as in FormsProfileMeta.surveys
            )

            survey = source_survey.clone(
                event=event,
                slug=str(input.survey_slug),
                app=app,
                purpose=purpose,
                anonymity=anonymity,
                created_by=request.user,  # type: ignore
            )
        else:
            survey = Survey(
                event=event,
                slug=input.survey_slug,
                app=app,
                purpose=purpose,
                anonymity=anonymity.value,
            ).with_mandatory_fields()
            survey.full_clean()  # Validate fields
            survey.save()

        survey.workflow.handle_new_survey()

        return CreateSurvey(survey=survey)  # type: ignore
