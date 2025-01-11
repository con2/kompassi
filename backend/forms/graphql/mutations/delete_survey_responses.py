import graphene

from access.cbac import graphql_check_instance

from ...models.survey import Survey


class DeleteSurveyResponsesInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    response_ids = graphene.List(graphene.String)
    all = graphene.Boolean()


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

        # TODO bastardization of graphql_check_access, rethink
        graphql_check_instance(survey, info, "responses", "delete")

        if input.all:
            queryset = survey.responses.all()
        elif input.response_ids:
            queryset = survey.responses.filter(id__in=input.response_ids)
        else:
            queryset = survey.responses.none()

        _, deleted_by_model = queryset.delete()
        count_deleted = deleted_by_model.get("forms.Response", 0)

        return DeleteSurveyResponses(count_deleted=count_deleted)  # type: ignore
