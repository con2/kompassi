import graphene

from access.cbac import graphql_check_instance

from ...models.survey import Survey


class DeleteSurveyInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)


class DeleteSurvey(graphene.Mutation):
    class Arguments:
        input = DeleteSurveyInput(required=True)

    slug = graphene.Field(graphene.String)

    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteSurveyInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)

        # TODO(#324) rethink
        graphql_check_instance(survey, info, "self", "mutation")
        if not survey.can_remove:
            raise Exception("Cannot delete survey")

        survey.delete()

        return DeleteSurvey(slug=input.survey_slug)  # type: ignore
