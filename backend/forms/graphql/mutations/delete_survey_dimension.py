import graphene

from access.cbac import graphql_check_access

from ...models.survey import Survey


class DeleteSurveyDimensionInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    dimension_slug = graphene.String(required=True)


class DeleteSurveyDimension(graphene.Mutation):
    class Arguments:
        input = DeleteSurveyDimensionInput(required=True)

    slug = graphene.Field(graphene.String)

    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteSurveyDimensionInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)

        # TODO bastardization of graphql_check_access, rethink
        graphql_check_access(survey, info, "dimensions", "mutation")

        dimension = survey.dimensions.get(slug=input.dimension_slug)
        if not dimension.can_remove:
            raise Exception("Cannot remove dimension that is in use")

        dimension.delete()

        return DeleteSurveyDimension(slug=input.survey_slug)  # type: ignore
