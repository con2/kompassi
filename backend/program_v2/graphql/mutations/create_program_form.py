import graphene

from access.cbac import graphql_check_model
from core.models import Event
from forms.graphql.mutations.create_survey import CreateSurveyInput
from forms.graphql.survey_full import SurveyType
from forms.models.survey import Survey


class CreateProgramForm(graphene.Mutation):
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

        graphql_check_model(
            Survey,
            event.scope,
            info,
            operation="create",
            app="program_v2",
        )

        survey = Survey(
            event=event,
            slug=input.survey_slug,
            app="program_v2",
            login_required=True,
            anonymity="name_and_email",
            key_fields=["title"],
        )
        survey.full_clean()
        survey.save()
        return CreateProgramForm(survey=survey)  # type: ignore
