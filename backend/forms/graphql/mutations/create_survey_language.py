import graphene

from access.cbac import graphql_check_instance

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
            app=survey.app,
            field="languages",
            operation="create",
        )

        if input.copy_from:
            form = survey.languages.get(language=input.copy_from)
            form.pk = None
            form.language = input.language
            form.created_by = info.context.user
            form.save()
        else:
            form = Form.objects.create(
                event=survey.event,
                survey=survey,
                language=input.language,
                created_by=info.context.user,
            )

        survey.workflow.handle_form_update()
        return CreateSurveyLanguage(form=form)  # type: ignore
