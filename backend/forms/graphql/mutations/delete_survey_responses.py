import graphene

from access.cbac import graphql_check_instance

from ...models.survey import Survey


class DeleteSurveyResponsesInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    response_ids = graphene.List(graphene.String)


class DeleteSurveyResponses(graphene.Mutation):
    class Arguments:
        input = DeleteSurveyResponsesInput(required=True)

    count_deleted = graphene.NonNull(graphene.Int)

    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteSurveyResponsesInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        graphql_check_instance(survey, info, "responses", "delete")

        queryset = survey.responses.filter(id__in=input.response_ids)
        _, deleted_by_model = queryset.delete()
        count_deleted = deleted_by_model.get("forms.Response", 0)

        return DeleteSurveyResponses(count_deleted=count_deleted)  # type: ignore
