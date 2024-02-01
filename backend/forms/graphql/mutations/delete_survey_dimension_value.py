import graphene

from access.cbac import graphql_check_access

from ...models.dimension import DimensionValue
from ...models.survey import Survey


class DeleteSurveyDimensionValueInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    dimension_slug = graphene.String(required=True)
    value_slug = graphene.String(required=True)


class DeleteSurveyDimensionValue(graphene.Mutation):
    class Arguments:
        input = DeleteSurveyDimensionValueInput(required=True)

    slug = graphene.Field(graphene.String)

    @staticmethod
    def mutate(
        root,
        info,
        input: DeleteSurveyDimensionValueInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)

        # TODO bastardization of graphql_check_access, rethink
        graphql_check_access(survey, info, "dimensions", "mutation")

        value = DimensionValue.objects.get(dimension__slug=input.dimension_slug, slug=input.value_slug)
        if not value.can_remove:
            raise Exception("Cannot remove dimension value that is in use")

        value.delete()

        return DeleteSurveyDimensionValue(slug=input.survey_slug)  # type: ignore
