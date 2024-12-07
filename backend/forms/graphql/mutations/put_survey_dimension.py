import graphene
from graphene.types.generic import GenericScalar

from access.cbac import graphql_check_instance

from ...models.dimension_dto import DimensionDTO
from ...models.survey import Survey
from ..dimension import SurveyDimensionType


class PutSurveyDimensionInput(graphene.InputObjectType):
    event_slug = graphene.String(required=True)
    survey_slug = graphene.String(required=True)
    dimension_slug = graphene.String(description="If set, update existing; otherwise, create new")
    form_data = GenericScalar(required=True)


class PutSurveyDimension(graphene.Mutation):
    class Arguments:
        input = PutSurveyDimensionInput(required=True)

    dimension = graphene.Field(SurveyDimensionType)

    @staticmethod
    def mutate(
        root,
        info,
        input: PutSurveyDimensionInput,
    ):
        survey = Survey.objects.get(event__slug=input.event_slug, slug=input.survey_slug)
        form_data: dict[str, str] = input.form_data  # type: ignore

        # TODO bastardization of graphql_check_access, rethink
        graphql_check_instance(survey, info, "dimensions", "mutation")

        if input.dimension_slug is None:
            if survey.dimensions.filter(slug=form_data["slug"]).exists():
                raise ValueError("Dimension with this slug already exists")
        else:
            form_data["slug"] = input.dimension_slug  # type: ignore

        dimension = DimensionDTO.from_form_data(form_data).save(survey)

        return PutSurveyDimension(dimension=dimension)  # type: ignore
