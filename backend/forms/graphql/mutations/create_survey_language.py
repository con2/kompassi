import graphene

from access.cbac import graphql_check_instance
from dimensions.models.enums import DimensionApp
from graphql_api.language import SUPPORTED_LANGUAGE_CODES
from program_v2.utils.default_fields import get_program_offer_form_default_fields

from ...models.enums import SurveyPurpose
from ...models.form import Form
from ...models.survey import Survey
from ..form import FormType


class CreateSurveyLanguageInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    language = graphene.String(required=True)
    copy_from = graphene.String()


class CreateSurveyLanguage(graphene.Mutation):
    class Arguments:
        input = CreateSurveyLanguageInput(required=True)

    form = graphene.Field(FormType)

    @staticmethod
    def mutate(
        root,
        info,
        input: CreateSurveyLanguageInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        graphql_check_instance(
            survey,
            info,
            app=survey.app_name,
            field="languages",
            operation="create",
        )

        language: str = input.language  # type: ignore
        if language not in SUPPORTED_LANGUAGE_CODES:
            raise ValueError(f"Unsupported language: {language}")

        if input.copy_from:
            form = survey.languages.get(language=input.copy_from)
            form.pk = None
            form.language = input.language
            form.created_by = info.context.user
            form.save()
        else:
            if survey.app == DimensionApp.PROGRAM_V2 and survey.purpose == SurveyPurpose.DEFAULT:
                fields = get_program_offer_form_default_fields(language)
            else:
                fields = []

            form = Form.objects.create(
                event=survey.event,
                survey=survey,
                language=input.language,
                created_by=info.context.user,
                fields=fields,
            )

        survey.workflow.handle_form_update()
        return CreateSurveyLanguage(form=form)  # type: ignore
