import graphene
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_access

from ...models.dimension import DimensionDTO
from ...models.survey import Survey
from ..dimension import SurveyDimensionType


class CreateSurveyDimensionInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    form_data = GenericScalar(required=True)


class CreateSurveyDimension(graphene.Mutation):
    class Arguments:
        input = CreateSurveyDimensionInput(required=True)

    dimension = graphene.Field(SurveyDimensionType)

    @staticmethod
    def mutate(
        root,
        info,
        input: CreateSurveyDimensionInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)

        # TODO bastardization of graphql_check_access, rethink
        graphql_check_access(survey, info, "dimensions", "mutation")

        form_data: dict[str, str] = input.form_data  # type: ignore
        print(form_data)
        dimension = DimensionDTO.from_form_data(form_data).save(survey)

        return CreateSurveyDimension(dimension=dimension)  # type: ignore
