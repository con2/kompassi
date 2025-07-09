import graphene
from django.http import HttpRequest

from ...models.survey import Survey


class DeleteSurveyLanguageInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    language = graphene.String(required=True)


class DeleteSurveyLanguage(graphene.Mutation):
    class Arguments:
        input = DeleteSurveyLanguageInput(required=True)

    language = graphene.Field(graphene.String)

    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteSurveyLanguageInput,
    ):
        request: HttpRequest = info.context
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)

        form = survey.languages.get(language=input.language)
        if not form.can_be_deleted_by(request):
            raise Exception("Cannot delete survey language")

        form.delete()

        survey.workflow.handle_form_update()
        return DeleteSurveyLanguage(language=input.language)  # type: ignore
