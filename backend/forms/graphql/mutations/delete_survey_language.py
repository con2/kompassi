import graphene

from access.cbac import graphql_check_instance

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
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)

        # TODO(#324) rethink
        graphql_check_instance(survey, info, "self", "mutation")

        form = survey.languages.get(language=input.language)
        if not form.can_remove:
            raise Exception("Cannot delete survey")

        form.delete()

        return DeleteSurveyLanguage(language=input.language)  # type: ignore
