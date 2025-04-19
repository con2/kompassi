import graphene
from django.http import HttpRequest

from access.cbac import graphql_check_instance, graphql_check_model
from core.models import Event
from forms.graphql.mutations.create_survey import CreateSurveyInput
from forms.graphql.survey_full import FullSurveyType
from forms.models.survey import Survey, SurveyApp


class CreateProgramFormInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    copy_from = graphene.String()


# TODO possibly unify with CreateSurvey?
class CreateProgramForm(graphene.Mutation):
    class Arguments:
        input = CreateProgramFormInput(required=True)

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
            app="program_v2",
        )

        if input.copy_from:
            source_event_slug, source_survey_slug = str(input.copy_from).split("/")
            source_survey = Survey.objects.get(
                event__slug=source_event_slug,
                slug=source_survey_slug,
            )

            graphql_check_instance(
                source_survey,
                info,
                app=source_survey.app,  # NOTE same check as in FormsProfileMeta.surveys
            )

            survey = source_survey.clone(
                event=event,
                slug=str(input.survey_slug),
                app=SurveyApp.PROGRAM_V2,
                created_by=request.user,  # type: ignore
            )
        else:
            survey = Survey(
                event=event,
                slug=input.survey_slug,
            ).with_mandatory_attributes_for_app(SurveyApp.PROGRAM_V2)
            survey.full_clean()  # Validate fields
            survey.save()

        survey.workflow.handle_form_update()
        return CreateProgramForm(survey=survey)  # type: ignore
